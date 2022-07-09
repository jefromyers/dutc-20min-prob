import { createRoot } from 'react-dom/client';
import React from 'react';
import {useState, useEffect} from 'react';

const API = 'http://127.0.0.1:8000/v1'

const Winner = () => {
  const [winner, setWinner] = useState(null)

  useEffect(
    () => {
      fetch(`${API}/winner`)
        .then(res => res.json())
        .then(data => setWinner(data.winner))
    }, []
  )

  return (
    <>
    <h4 className="text-4xl font-extrabold text-green-500">Winner: {(winner) ? winner : 'Still thinking'}</h4>
    </>
  )
}

const Restaurants = () => {
  const [restaurant, setRestaurant] = useState([])

  useEffect(
    () => {
      fetch(`${API}/restaurants`)
        .then(res => res.json())
        .then(data => setRestaurant(data.restaurants))
    }, []
  )

  return (
    <>
    <h4 className="text-2xl font-extrabold text-gray-900 tracking-tight sm:text-2xl">Restaurants:</h4>
    <table className="mb-3">
      <tbody> 
        {
          restaurant.map(n => <tr key={n}><td>{n}</td></tr>)
        }
      </tbody>
    </table>
    </>
  )
}

const Team = () => {

  const [team, setTeam] = useState([])
  useEffect(
    () => {
      fetch(`${API}/team`)
        .then(res => res.json())
        .then(data => setTeam(data.team))
    }, []
  )
  
  return (
    <>
    <h4 className="text-2xl font-extrabold text-gray-900 tracking-tight sm:text-2xl">Team:</h4>
    <table className="table-fixed w-full mb-3">
      <thead className="text-left"> 
        <tr>
          <th scope='col' className="w-[125px] px-3 py-3">Name</th>
          <th scope='col' className="px-3 py-3">Really Like</th>
          <th scope='col' className="px-3 py-3">Like</th>
          <th scope='col' className="px-3 py-3">Dislike</th>
        </tr>
      </thead>
      <tbody> 
        {
          team.map(t => <tr key={t.name}>
            <td scope='row' className="px-3 py-3">{t.name}</td>
            <td scope='row' className="px-3 py-3">
              {
                (t.RL.length > 0) ? t.RL.map(p => <span>{p}, </span>) : ''
              }
            </td>
            <td scope='row' className="px-3 py-3">
              {
                (t.L.length > 0) ? t.L.map(p => <span>{p}, </span>) : ''
              }
            </td>
            <td scope='row' className="px-3 py-3">
              {
                (t.DL.length > 0) ? t.DL.map(p => <span>{p}, </span>) : ''
              }
            </td>
            </tr>)
        }
      </tbody>
    </table>
    </>
  )
}

const App = () => {
  return ( 
    <div className="max-w-7xl mx-auto sm:px-6 lg:px-8 mt-4">
      <Winner />
      <Restaurants />
      <Team />
    </div>
  )
}


const root = createRoot(document.getElementById('root'))
root.render(<App />)
