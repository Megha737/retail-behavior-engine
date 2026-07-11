import React, { useState } from 'react';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    // This connects to the backend we will build in Step 2
    const response = await fetch('http://127.0.0.1:8000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      onLogin(); // Tell App.js the user is authenticated
    } else {
      alert("Invalid credentials!");
    }
  };

  return (
    <div className="login-box bento-box" style={{ maxWidth: '300px', margin: '20vh auto' }}>
      <h3>Login</h3>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
        <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
        <button type="submit" className="theme-toggle">Sign In</button>
      </form>
    </div>
  );
}
export default Login;