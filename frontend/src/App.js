import React from 'react'
import UploadDiagnose from './components/UploadDiagnose'
import PlantDatabase from './components/PlantDatabase'
import Dashboard from './components/Dashboard'
import './styles.css'

export default function App() {
  return (
    <div className="app-root">
      <header className="app-header">
        <h1>Smart Plant Care Assistant</h1>
        <p>Upload a photo or describe symptoms to get a diagnosis and care tips</p>
      </header>
      <main className="main-grid">
        <section className="left">
          <UploadDiagnose />
          <PlantDatabase />
        </section>
        <aside className="right">
          <Dashboard />
        </aside>
      </main>
      <footer className="app-footer">Made with care by Harsh Tayal</footer>
    </div>
  )
}
