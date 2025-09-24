import React, { useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import Sidebar from './components/Sidebar';
import Workspace from './components/Workspace';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [activeTab, setActiveTab] = useState('chat');

  return (
    <Container fluid className="vh-100">
      <Row className="h-100">
        {/* Sidebar Column */}
        <Col xs={1} style={{ width: '150px' }} className="p-0 bg-dark text-white">
          <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        </Col>

        {/* Workspace Column */}
        <Col xs={10} className="">
          <Workspace activeTab={activeTab} />
        </Col>
      </Row>
    </Container>
  );
}

export default App;
