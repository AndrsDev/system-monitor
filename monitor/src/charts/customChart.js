import React from "react";
import { Chart } from "react-charts";

function CustomChart({plots}) {


  const data = React.useMemo(
    () => [
      {
        label: "CPU %",
        data: plots
      }
    ],
    [plots]
  );

  const axes = React.useMemo(
    () => [
      { primary: true, type: "linear", position: "bottom" },
      { type: "linear", position: "left" },
    ],
    []
  );

  return (
    <div className="chart-container">
      <Chart data={data} axes={axes} dark tooltip />
    </div>
  )


}

export default CustomChart;