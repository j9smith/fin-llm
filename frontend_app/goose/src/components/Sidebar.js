import React, {useState} from 'react';
import { Nav } from 'react-bootstrap';
import LoginForm from './LoginForm';
import RegistrationForm from './RegistrationForm';

function Sidebar({ activeTab, setActiveTab }) {
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [showRegistrationForm, setShowRegistrationForm] = useState(false);

  return (
    <>
      <div className="d-flex flex-column bg-dark text-white vh-100 p-3">
        <h2 className="text-white mb-4" aria-hidden="true"></h2>
        <div className="mb-4 d-flex align-items-center">
          <Nav.Item>
            <Nav.Link
              onClick={() => setShowLoginForm(true)}
              className="text-white small"
            >
              Login
            </Nav.Link>
          </Nav.Item>
          <span className="text-white mx-2">|</span>
          <Nav.Item>
            <Nav.Link
              onClick={() => setShowRegistrationForm(true)}
              className="text-white small"
            >
              Register
            </Nav.Link>
          </Nav.Item>
        </div>

        <Nav variant="pills" className="flex-column">
          <Nav.Item>
            <Nav.Link
              eventKey="chat"
              active={activeTab === 'chat'}
              onClick={() => setActiveTab('chat')}
              className="text-white"
            >
              Workspace
            </Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link
              eventKey="content"
              active={activeTab === 'content'}
              onClick={() => setActiveTab('content')}
              className="text-white"
            >
              Content
            </Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link
              eventKey="info"
              active={activeTab === 'info'}
              onClick={() => setActiveTab('info')}
              className="text-white"
            >
              Info
            </Nav.Link>
          </Nav.Item>
        </Nav>
      </div>

      {showLoginForm && (
        <>
          <div className="overlay" onClick={() => setShowLoginForm(false)} />
          <LoginForm onClose={() => setShowLoginForm(false)} />
        </>
      )}
      {showRegistrationForm && (
        <>
          <div className="overlay" onClick={() => setShowRegistrationForm(false)} />
          <RegistrationForm onClose={() => setShowRegistrationForm(false)} />
        </>
      )}
    </>
  );
}

export default Sidebar;
