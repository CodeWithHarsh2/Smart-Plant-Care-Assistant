import axios from 'axios'

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:5000'

export const uploadImage = (file) => {
  const fd = new FormData()
  fd.append('image', file)
  return axios.post(`${API_BASE}/api/upload`, fd)
}

export const diagnoseText = (text) => axios.post(`${API_BASE}/api/diagnose-text`, { text })

export const getWeather = (lat, lon) => axios.get(`${API_BASE}/api/weather?lat=${lat}&lon=${lon}`)
