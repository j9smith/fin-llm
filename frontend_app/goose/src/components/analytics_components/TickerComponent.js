// TickerComponent.js
import React from 'react';

function TickerComponent({ uiElement }) {
  return (
    <div className="widget-container">
      <div className="stock-price-element">
        <h3>{uiElement.ui_title}</h3>
        <p>Last updated stock price: ${uiElement.ui_content}</p>
      </div>
    </div>
  );
}

export default TickerComponent;
