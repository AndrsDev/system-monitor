import React, { useEffect, useState } from "react";
import firebase from "./firebase";
import "./App.css";
import CustomChart from "./charts/customChart";

const db = firebase.database();

function App() {
  const [data, setData] = useState({});
  const [cpuUsage, setCpuUsage] = useState([[0,0]]);
  const [ramUsage, setRamUsage] = useState([[0,0]]);
  const [diskUsage, setDiskUsage] = useState([[0,0]]);
  const [networkUsage, setNetworkUsage] = useState([[0,0]]);

  let seconds = 0;

  useEffect(() => {
    const ref = db.ref();
    ref.on("value", (snapshot) => {
      setData(snapshot.val());
      seconds++;  
      setCpuUsage(cpuUsage => cpuUsage.concat([[seconds, snapshot.val()?.cpu?.percentage ?? 0]]))
      setRamUsage(ramUsage => ramUsage.concat([[seconds, snapshot.val()?.ram?.percentage ?? 0]]))
      setDiskUsage(diskUsage => diskUsage.concat([[seconds, snapshot.val()?.ram?.percentage ?? 0]]))
      setNetworkUsage(networkUsage => networkUsage.concat([[seconds, snapshot.val()?.network?.packets_received ?? 0]]))
    });

    return function cleanup() {
      ref.off();
    };
  }, [seconds]);

  const getGrowRate = (values) => {
    if(values.length > 1){
      return Math.round((values[values.length - 1][1] - values[values.length - 2][1]) * 100)/100
    }
    return 0
  }

  const getScore = () => {
    if(cpuUsage.length > 1){
      let cpu = cpuUsage[cpuUsage.length - 1][1];
      let ram = ramUsage[ramUsage.length - 1][1];
      let disk = diskUsage[diskUsage.length - 1][1];

      let average = (cpu + ram + disk) / 3;

      return Math.round(100 - average * 0.2)
    }
    return 0
  }

  return (
    <div className="app">
      <div className="content">
        <h1>System Monitor</h1>
        <p>
          <strong>Node: </strong> {data?.information?.node}
        </p>
        <p>
          <strong>System: </strong> {data?.information?.system}
        </p>
        <p>
          <strong>Version: </strong> {data?.information?.version}
        </p>
        <p>
          <strong>Release: </strong> {data?.information?.release}
        </p>
        <p>
          <strong>Machine: </strong> {data?.information?.machine}
        </p>
        <p>
          <strong>Processor: </strong> {data?.information?.processor}
        </p>
        <p>
          <strong>Boot Time: </strong> {data?.information?.boot_time}
        </p>

        <div className="cards-grid">
          <div className="card">
           
      
            <div className="stats">
              <h2>CPU</h2>
              <p>
                <strong>Physical Cores: </strong> {data?.cpu?.physical_cores}
              </p>
              <p>
                <strong>Total Cores: </strong> {data?.cpu?.total_cores}
              </p>
              <p>
                <strong>Min: </strong> {data?.cpu?.min} MHz
              </p>
              <p>
                <strong>Max: </strong> {data?.cpu?.max} MHz
              </p>
              <p>
                <strong>Current: </strong> {data?.cpu?.current} MHz
              </p>
              <p>
                <strong>Percentage: </strong> {data?.cpu?.percentage} %
              </p>
              <p>
                <strong>Grow Rate: </strong> {getGrowRate(cpuUsage)} p/s
              </p>

            </div>
            <CustomChart plots={cpuUsage}/>
          </div>

          <div className="card">
            <div className="stats">
              <h2>RAM</h2>
              <p>
                <strong>Total: </strong> {data?.ram?.total}
              </p>
              <p>
                <strong>Used: </strong> {data?.ram?.used}
              </p>
              <p>
                <strong>Available: </strong> {data?.ram?.available}
              </p>
              <p>
                <strong>Percentage: </strong> {data?.ram?.percentage} %
              </p>
              <p>
                <strong>Grow Rate: </strong> {getGrowRate(ramUsage)} p/s
              </p>
            </div>
            <CustomChart plots={ramUsage}/>
          </div>

          <div className="card">
            <div className="stats">
              <h2>DISK</h2>
              <p>
                <strong>Total Size: </strong> {data?.disk?.total_size}
              </p>
              <p>
                <strong>Used: </strong> {data?.disk?.used}
              </p>
              <p>
                <strong>Free: </strong> {data?.disk?.free}
              </p>
              <p>
                <strong>Total Read: </strong> {data?.disk?.total_read}
              </p>
              <p>
                <strong>Total Write: </strong> {data?.disk?.total_write}
              </p>
              <p>
                <strong>Percentage: </strong> {data?.disk?.percentage} %
              </p>
              <p>
                <strong>Grow Rate: </strong> {getGrowRate(diskUsage)} p/s
              </p>
            </div>
            <CustomChart plots={diskUsage}/>
          </div>

          <div className="card">
            <div className="stats">
              <h2>NETWORK</h2>
              <p>
                <strong>Total Sent: </strong> {data?.network?.total_sent}
              </p>
              <p>
                <strong>Total Received: </strong> {data?.network?.total_received}
              </p>
              <p>
                <strong>Packets Sent: </strong> {data?.network?.packets_sent}
              </p>
              <p>
                <strong>Packets Received: </strong> {data?.network?.packets_received}
              </p>
              <p>
                <strong>Grow Rate: </strong> {getGrowRate(networkUsage)} p/s
              </p>
            </div>
            <CustomChart plots={networkUsage}/>
          </div>
        </div>

        <div className="score">
          <p className="big-text">{getScore()}/100</p>
          <p className="small-text">Score</p>
        </div>
      
      </div>
    </div>
  );
}

export default App;
