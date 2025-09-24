// import React from 'react';
// import TickerComponent from './analytics_components/TickerComponent';

// function AnalyticsSpace({ activeUIElement }) {
//   return (
//     <div className="p-3 border bg-light">
//       <h3>Analytics Space</h3>

//       {activeUIElement ? (
//         <div className = "widget-container-space">
//           {activeUIElement.ui_type === 'ticker' && (
//             <TickerComponent uiElement={activeUIElement} />
//           )}
//           {/* ADD MORE COMPONENTS HERE */}
//     </div>
//   ) : (
//     <p>No UI elements selected</p>
//   )}
//   </div>
//   );
// }

// export default AnalyticsSpace;

import React, { useState, useEffect } from 'react';
import { Tabs, Tab, Button } from 'react-bootstrap';
import TickerComponent from './analytics_components/TickerComponent';
import HistoricalChartComponent from './analytics_components/HistoricalChartComponent';

function AnalyticsSpace({ activeUIElement }) {
  const [activeTabs, setActiveTabs] = useState([]); // State to manage open tabs
  const [activeKey, setActiveKey] = useState('default'); // State for currently active tab key

  useEffect(() => {
    if (activeUIElement) {
      const exists = activeTabs.some(tab => tab.ui_title === activeUIElement.ui_title);
  
      if (!exists) {
        setActiveTabs(prevTabs => {
          const newTabs = [...prevTabs, activeUIElement];
          return newTabs;
        });
        setActiveKey(activeUIElement.ui_title);
      } else {
        setActiveKey(activeUIElement.ui_title);
      }
    }
  }, [activeUIElement]);

  // Function to handle closing a tab
  const handleCloseTab = (tabTitle) => {
    setActiveTabs(prevTabs => prevTabs.filter(tab => tab.ui_title !== tabTitle));
    // If the closed tab is the active tab, set the active key to the default or another existing tab
    if (activeKey === tabTitle) {
      setActiveKey(activeTabs.length > 1 ? activeTabs[0].ui_title : 'default');
    }
  };

  return (
    <div className="p-3 border bg-light">
      <Tabs
        id="analytics-tabs"
        activeKey={activeKey}
        onSelect={(k) => setActiveKey(k)}
        className="mb-3"
      >
        {/* Default tab with initial message */}
        <Tab eventKey="default" title="Welcome">
          <div>
            <p>Analytics load here. Select or trigger an analysis to open tabs.</p>
          </div>
        </Tab>

        {/* Render a tab for each active UI element */}
        {activeTabs.map((tab, index) => (
          <Tab
            key={tab.ui_title || index}
            eventKey={tab.ui_title}
            title={
              <>
                {tab.ui_title}
                <Button
                  variant="link"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation(); // Prevent switching tabs when clicking the button
                    handleCloseTab(tab.ui_title);
                  }}
                  style={{ padding: 0, marginLeft: '5px', color: 'red' }}
                >
                  x
                </Button>
              </>
            }
          >
            <div>
              {tab.ui_type === 'ticker' && <TickerComponent uiElement={tab} />}
              {tab.ui_type === 'line_chart' && <HistoricalChartComponent uiElement={tab} />}
              {/* Add more conditions for other component types */}
            </div>
          </Tab>
        ))}
      </Tabs>
    </div>
  );
}

export default AnalyticsSpace;
