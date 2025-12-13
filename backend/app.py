from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from utils import save_image
from diagnosis import diagnose_from_image, diagnose_from_text
from scheduler import start_scheduler, schedule_watering
import sqlite3
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
from health_score import compute_health_score
from context_analysis import analyze_context


load_dotenv()

OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY') or ''

app = Flask(__name__)
@app.route("/")
def index():
    return "Smart Plant Care Assistant backend is running"

CORS(app)

BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# simple sqlite helper
DB_PATH = os.path.join(BASE_DIR, 'database.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS plants (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 species TEXT,
                 last_watered TEXT,
                 watering_interval_days INTEGER,
                 notes TEXT
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 plant_id INTEGER,
                 timestamp TEXT,
                 action TEXT,
                 details TEXT
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS plant_health_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_id INTEGER,
                timestamp TEXT,
                health_score INTEGER,
                diagnosis_summary TEXT,
                risk_prediction TEXT
                 )''')
    print("Database initialized, tables ensured")
    conn.commit()
    conn.close()

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'no file part'}), 400
    f = request.files['image']
    if f.filename == '':
        return jsonify({'error': 'no selected file'}), 400
    path = save_image(f)
    result = diagnose_from_image(path)
        # STEP 4: HEALTH SCORE CALCULATION

    # 1. Visual confidence (best diagnosis probability)
    visual_confidence = max([d["probability"] for d in result])

    # 2. Temporary scores (will improve later)
    watering_score = 0.7
    weather_score = 0.8
    plant_match_score = 0.75

    # 3. Compute final health score
    health_score = compute_health_score(
        visual_confidence,
        watering_score,
        weather_score,
        plant_match_score
    )
    return jsonify({
        'diagnosis': result,
        'health_score': health_score
    })

@app.route('/api/diagnose-text', methods=['POST'])
def diagnose_text():
    data = request.json
    txt = data.get('text', '')
    result = diagnose_from_text(txt)
    return jsonify({'diagnosis': result})

@app.route('/api/weather', methods=['GET'])
def weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon or not OPENWEATHER_API_KEY:
        return jsonify({'error': 'missing lat/lon or API key'}), 400
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&units=metric&appid={OPENWEATHER_API_KEY}'
    r = requests.get(url)
    return jsonify(r.json())

@app.route('/api/plants', methods=['POST'])
def add_plant():
    data = request.json
    name = data.get('name')
    species = data.get('species')
    interval = data.get('watering_interval_days', 3)
    now = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO plants (name, species, last_watered, watering_interval_days, notes) VALUES (?,?,?,?,?)',
              (name, species, now, interval, data.get('notes', '')))
    plant_id = c.lastrowid
    conn.commit()
    conn.close()
    # schedule first watering reminder
    next_run = datetime.utcnow() + timedelta(days=interval)
    # placeholder callback
    def reminder(pid=plant_id):
        print('Reminder: water plant', pid)
    schedule_watering(plant_id, next_run, reminder)
    return jsonify({'status': 'ok', 'plant_id': plant_id})

@app.route('/api/plants', methods=['GET'])
def list_plants():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, species, last_watered, watering_interval_days, notes FROM plants')
    rows = c.fetchall()
    conn.close()
    plants = []
    for r in rows:
        plants.append({
            'id': r[0],
            'name': r[1],
            'species': r[2],
            'last_watered': r[3],
            'watering_interval_days': r[4],
            'notes': r[5]
        })
    return jsonify({'plants': plants})

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    init_db()
    start_scheduler(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
