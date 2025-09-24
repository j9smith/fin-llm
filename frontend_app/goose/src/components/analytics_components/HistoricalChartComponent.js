// HistoricalChartComponent.js
import React from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );

function HistoricalChartComponent({ uiElement }) {
  if (!uiElement || !uiElement.ui_content) {
    return <p>No data available for charting.</p>;
  }

  // Extract data for the chart
  const dates = uiElement.ui_content.map(dataPoint => dataPoint.date);
  const prices = uiElement.ui_content.map(dataPoint => dataPoint.close);

  // Prepare chart data
  const data = {
    labels: dates,
    datasets: [
      {
        label: uiElement.ui_title || 'Stock Price Over Time',
        data: prices,
        fill: false,
        backgroundColor: '#FF5733', // Chart line color
        borderColor: '#FF5733',
        tension: 0.1,
        pointRadius: 0,
      },
    ],
  };

  // Chart options
  const options = {
    scales: {
      x: {
        title: {
          display: true,
          text: 'Date',
        },
        type: 'category',
      },
      y: {
        title: {
          display: true,
          text: 'Price',
        },
      },
    },
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
    },
  };

  return (
    <div className="widget-container">
      <h3>{uiElement.ui_title}</h3>
      <Line data={data} options={options} />
    </div>
  );
}

export default HistoricalChartComponent;