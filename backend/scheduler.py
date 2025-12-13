from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()

# Example job storage
WATERING_JOBS = {}

def start_scheduler(app):
    scheduler.start()

def schedule_watering(plant_id, next_run, callback, *args, **kwargs):
    # next_run is a datetime
    job = scheduler.add_job(callback, 'date', run_date=next_run, args=args, kwargs=kwargs)
    WATERING_JOBS[plant_id] = job
    return job

def cancel_watering(plant_id):
    job = WATERING_JOBS.get(plant_id)
    if job:
        job.remove()
        del WATERING_JOBS[plant_id]
        return True
    return False
