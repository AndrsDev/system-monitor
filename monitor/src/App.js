import { useEffect, useState } from 'react';
import firebase from './firebase';
import './app.css';

const db = firebase.database();

function App() {

  const [data, setData] = useState({});

  useEffect(() => {

    const ref = db.ref();
    ref.on('value', (snapshot) => {
      setData(snapshot.val())
    });

    return function cleanup() {
      ref.off();
    };
  },[]);

  return (
    <div className="app">
      <div className="content"> 
        <h1>System Monitor</h1>
        <p><strong>Node: </strong> {data?.information?.node}</p>
        <p><strong>System: </strong> {data?.information?.system}</p>
        <p><strong>Version: </strong> {data?.information?.version}</p>
        <p><strong>Release: </strong> {data?.information?.release}</p>
        <p><strong>Machine: </strong> {data?.information?.machine}</p>
        <p><strong>Processor: </strong> {data?.information?.processor}</p>
        <p><strong>Boot Time: </strong> {data?.information?.boot_time}</p>

        <div className="cards-grid">
          <div className="card">
            <h2>CPU</h2>
            <p><strong>Physical Cores: </strong> {data?.cpu?.physical_cores}</p>
            <p><strong>Total Cores: </strong> {data?.cpu?.total_cores}</p>
            <p><strong>Min: </strong> {data?.cpu?.min} MHz</p>
            <p><strong>Max: </strong> {data?.cpu?.max} MHz</p>
            <p><strong>Current: </strong> {data?.cpu?.current} MHz</p>
            <p><strong>Percentage: </strong> {data?.cpu?.percentage} %</p>
          </div>
          <div className="card">
            <h2>RAM</h2>
            <p><strong>Total: </strong> {data?.ram?.total}</p>
            <p><strong>Used: </strong> {data?.ram?.used}</p>
            <p><strong>Available: </strong> {data?.ram?.available}</p>
            <p><strong>Percentage: </strong> {data?.ram?.percentage} %</p>
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;
