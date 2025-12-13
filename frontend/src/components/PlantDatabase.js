import React, { useEffect, useState } from 'react'
import { getPlants, addPlant } from '../api'

export default function PlantDatabase() {
  const [plants, setPlants] = useState([])
  const [name, setName] = useState('')
  const [species, setSpecies] = useState('')

  async function fetch() {
    const res = await getPlants()
    setPlants(res.data.plants)
  }

  useEffect(() => { fetch() }, [])

  async function handleAdd(e) {
    e.preventDefault()
    await addPlant({ name, species, watering_interval_days: 3 })
    setName('')
    setSpecies('')
    fetch()
  }

  return (
    <div className="card fade-in">
      <h3>Your Plants</h3>
      <form onSubmit={handleAdd}>
        <input className="input" placeholder="Plant name" value={name} onChange={e=>setName(e.target.value)} />
        <div style={{ height: 8 }} />
        <input className="input" placeholder="Species or notes" value={species} onChange={e=>setSpecies(e.target.value)} />
        <div style={{ height: 8 }} />
        <button className="button">Add Plant</button>
      </form>

      <div style={{ height: 12 }} />
      {plants.map(p => (
        <div key={p.id} style={{ padding: 8, borderBottom: '1px solid #eee' }}>
          <strong>{p.name}</strong>
          <div>{p.species}</div>
          <div>Water every {p.watering_interval_days} days</div>
        </div>
      ))}
    </div>
  )
}
