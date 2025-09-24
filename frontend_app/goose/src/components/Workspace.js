import React, { useState }  from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import ChatContainer from './ChatContainer';
import AnalyticsSpace from './AnalyticsSpace';
import NewsSpace from './NewsSpace';
function Workspace({ activeTab }) {
  const [activeUIElement, setActiveUIElement] = useState(null);
  const [newsData, setNewsData] = useState(null); 

  return (    
    <Container fluid className="vh-100 p-3" style={{ maxHeight: '100vh', overflow: 'hidden' }}>
    {/* <Container> is a wrapper for other elements and helps structure the page */}
    {/* fluid attribute makes the container extend to 100% width of viewport or parent element */}
    {/* overflow: hidden specifies that any content inside the container that overflows is hidden */}

      {/* Everything under activeTab == 'chat' will show when the 'chat' tab is selected */}
      {activeTab === 'chat' && (
        <Row className="h-100"> {/* Defines a row with height of 100% of parent container (we only need 1 row to contain our workspace elements) */}

          {/* Left half for the chat container */}
          {/* 'p-3' specifies padding of size 3 (bootstrap size, 16px). bg-light sets the background colour of the column. */ }
          {/* h-100 sets the height to 100% of the parent container. border-start puts border on LHS, -end on RHS */}
          <Col xs={6} className="p-3 bg-light h-100 border">
            <ChatContainer activeUIElement = {activeUIElement} setActiveUIElement = {setActiveUIElement} setNewsData={setNewsData}/> {/* Specifies the ChatContainer component should be loaded in this column with width xs={6} */}
          </Col>

          {/* Right column - Analytics and News */}
          {/* Right column - Analytics and News */}
          <Col xs={6} className="workspace-right-column p-0" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}> {/* Added p-0 to remove padding */}
            <div className="analytics-section" style={{ flex: '0 0 auto' }}>
              <AnalyticsSpace 
                activeUIElement={activeUIElement} 
                setActiveUIElement={setActiveUIElement}
              />
            </div>
            <div className="news-section" style={{ flex: '1 1 auto', overflow: 'auto' }}>
              <NewsSpace activeNewsData={newsData}/>
            </div>
          </Col>    
        </Row>
      )}

      {/* When the 'content' tab is selected */}
      {activeTab === 'content' && (
        <div className="h-100 d-flex justify-content-center align-items-center">
          <h2>Stay tuned for blog posts and news summaries</h2>
        </div>
      )}

      {/* When the 'info' tab is selected */}
      {activeTab === 'info' && (
        <div className="h-100 d-flex flex-column justify-content-center align-items-center text-center p-4">
          <h2 className="mb-4" style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>
            Welcome to Goosed Financial Advisory
          </h2>

          <section className="mb-4" style={{ maxWidth: '700px', lineHeight: '1.6' }}>
            <p style={{ fontSize: '1.2rem' }}>
              <strong>Empower Your Decisions</strong> with real-time insights into the financial markets. 
              At Goosed, our mission is to provide <span style={{ color: '#FF5733' }}>powerful tools </span> 
              and <span style={{ color: '#FF5733' }}>in-depth analytics</span> to guide your investment journey.
            </p>
          </section>

          <section className="mb-4" style={{ maxWidth: '700px', lineHeight: '1.6' }}>
            <h3 style={{ color: '#00CFFF', fontSize: '1.5rem' }}>Explore Our Features</h3>
            <ul style={{ textAlign: 'left', listStyleType: 'none', paddingLeft: 0 }}>
              <li style={{ marginBottom: '0.5rem' }}>
                📈 <strong>Advanced Analytics Tools</strong>: Analyze real-time and historical data across stocks, 
                derivatives, commodities, and more.
              </li>
              <li style={{ marginBottom: '0.5rem' }}>
                🕒 <strong>Real-Time Market Data</strong>: Stay updated with minute-by-minute market changes and price fluctuations.
              </li>
              <li style={{ marginBottom: '0.5rem' }}>
                📊 <strong>Customizable Dashboards</strong>: Tailor your experience with views and reports to suit your investment strategy.
              </li>
            </ul>
          </section>

          <section className="mb-4" style={{ maxWidth: '700px', lineHeight: '1.6' }}>
            <h3 style={{ color: '#00CFFF', fontSize: '1.5rem' }}>Why Choose Goosed?</h3>
            <p style={{ fontSize: '1.2rem' }}>
              Whether you’re an individual investor or a seasoned financial analyst, Goosed equips you 
              with insights and analytics designed to <span style={{ color: '#FF5733' }}>navigate the market with confidence</span>. 
              Our platform provides resources that adapt to your needs, helping you unlock opportunities in today’s fast-moving financial landscape.
            </p>
          </section>

          <p style={{ maxWidth: '700px', fontSize: '1.2rem', fontWeight: 'bold', color: '#FF5733' }}>
            Discover how Goosed Financial Advisory can turn data into actionable insights. Get started today!
          </p>
        </div>
      )}
    </Container>
  );
}

export default Workspace;
