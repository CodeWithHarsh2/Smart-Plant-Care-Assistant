import React, { useState } from 'react'
import { uploadImage, diagnoseText } from '../api'

export default function UploadDiagnose() {
  const [file, setFile] = useState(null)
  const [diagnosis, setDiagnosis] = useState(null)
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleUpload(e) {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    try {
      const res = await uploadImage(file)
      setDiagnosis(res.data.diagnosis)
    } catch (err) {
      alert('Upload failed: ' + err.message)
    } finally { setLoading(false) }
  }

  async function handleTextDiagnose(e) {
    e.preventDefault()
    if (!text) return
    setLoading(true)
    try {
      const res = await diagnoseText(text)
      setDiagnosis(res.data.diagnosis)
    } catch (err) {
      alert('Failed: ' + err.message)
    } finally { setLoading(false) }
  }

  return (
    <div className="card fade-in">
      <h3>Diagnose Plant</h3>
      <form onSubmit={handleUpload}>
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files[0])} />
        <div style={{ height: 10 }} />
        <button className="button" disabled={loading}>Upload Image</button>
      </form>

      <div style={{ height: 14 }} />
      <form onSubmit={handleTextDiagnose}>
        <input className="input" placeholder="Describe symptoms: yellow leaves, spots, droop" value={text} onChange={e => setText(e.target.value)} />
        <div style={{ height: 10 }} />
        <button className="button" disabled={loading}>Diagnose from text</button>
      </form>

      <div style={{ height: 12 }} />
      {diagnosis && (
        <div>
          <h4>Results</h4>
          {diagnosis.map((d, i) => (
            <div key={i} style={{ marginBottom: 8 }}>
              <strong>{d.issue}</strong>
              <div>Confidence: {(d.probability*100).toFixed(0)}%</div>
              <ul>
                {d.advice.map((a, j) => <li key={j}>{a}</li>)}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
