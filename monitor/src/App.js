import { useEffect, useState } from 'react';
import firebase from './firebase';
import './app.css';

const db = firebase.database();

function App() {

  const [data, setData] = useState({});

  useEffect(() => {

    const ref = db.ref('data');
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
        <h3 className="spacing-top">General Information</h3>
        {JSON.stringify(data)}
      </div>
    </div>
  );
}

export default App;
