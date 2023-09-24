import React, { useState } from 'react';
import { postData } from './httpService';
import './Login.css';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const payload = { username, password };
            const response = await postData('/login', payload);
            localStorage.setItem('access_token', response.access_token);
        } catch (error) {
            console.error('Login Failed:', error);
        }
    };
    return (
        <div className="login-container">
        <form className="login-form" onSubmit={handleSubmit}>
          <label className="login-label">
            Username:
            <input 
              className="login-input"
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)}
            />
          </label>
          <label className="login-label">
            Password:
            <input 
              className="login-input"
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <button className="login-button" type="submit">Login</button>
        </form>
      </div>
    );
  };
  
export default Login;
