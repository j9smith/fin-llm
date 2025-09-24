import React, { useState } from 'react';

function LoginForm({ onClose }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const apiUrl = process.env.REACT_APP_API_URL; 
  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
      const response = await fetch(`${apiUrl}/auth/jwt/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        credentials: 'include',
        body: formData.toString(),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Login successful:', data);
        // Handle successful login (e.g., store token, redirect)
      } else {
        console.error('Login failed');
        // Handle login failure
      }
    } catch (error) {
      console.error('Error:', error);
    }
    onClose();
  };

  return (
    <div className="position-fixed top-50 start-50 translate-middle bg-white p-4 rounded shadow-lg text-dark" style={{ zIndex: 1050 }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="login-email" className="form-label">Email</label>
          <input
            type="text"
            id="login-username"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="login-password" className="form-label">Password</label>
          <input
            type="password"
            id="login-password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">Login</button>
        <button type="button" className="btn btn-secondary ms-2" onClick={onClose}>Close</button>
      </form>
    </div>
  );
}

export default LoginForm;
