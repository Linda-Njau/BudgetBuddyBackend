import React, { useState } from 'react';
import { postData } from './httpService';

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
        <form onSubmit={handleSubmit}>
            <label>
                Username:
                <input type="text" value={username} onChange={(e) =>setUsername(e.target.value)}/>
            </label>
            <label>
                Password:
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}/>
            </label>
            <button type="submit">Login</button>
        </form>
    );
};
export default Login;
