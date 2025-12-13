import React from 'react'

export default function Dashboard() {
  return (
<div className="card fade-in">
  <h3>Plant Insights</h3>

  <div className="dashboard-stat">
    🌿 Healthy Plants Increase Survival Rate
  </div>

  <div className="dashboard-stat">
    💧 Smart Watering Prevents Overwatering
  </div>

  <div className="dashboard-stat">
    ☀️ Seasonal Care Improves Growth
  </div>

  <p style={{ marginTop: 12, color: "white" }}>
    This dashboard will later show analytics, reminders, and growth trends.
  </p>
</div>

  )
}
