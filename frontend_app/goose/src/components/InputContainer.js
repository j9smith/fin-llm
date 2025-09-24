import React from 'react';

function InputContainer({ input, setInput, handleSendMessage }) {
  return (
    <div className="input-group">
      <input
        type="text"
        className="form-control"
        placeholder="Type a message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
      />
      <button className="btn btn-primary" onClick={handleSendMessage}>Send</button>
    </div>
  );
}

export default InputContainer;
