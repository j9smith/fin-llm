import React from 'react';

function ChatWindow({ messages }) {
  return (
    <div className="chat-window border mb-3 p-2" style={{ maxHeight: '100vh', overflowY: 'auto' }}>
      {messages.map((msg, index) => (
        <div key={index} className={`message ${msg.sender === 'user' ? 'text-end' : 'text-start'}`}>
          <div className={`p-2 mb-1 ${msg.sender === 'user' ? 'bg-primary text-white rounded-pill' : 'bg-secondary text-white rounded-pill'}`}>
            {msg.text}
          </div>
        </div>
      ))}
    </div>
  );
}

export default ChatWindow;
