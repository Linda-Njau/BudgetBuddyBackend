import React, { useState } from 'react';
import { postData } from './httpService';

const UserSignUp = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const payload = {
                email: email,
                password: password,
                username: username,
            };
            const response = await postData('/users', payload);
            console.log('User Creation Response:', response);
        } catch (error) {
            console.error('User Creation Error:', error);
    }
};
return (
    <div>
        <h2>Create a New User</h2>
        <form onSubmit={handleSubmit}>
            <label>
                Email:
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
            </label>
            <label>
                Password:
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
            </label>
            <label>
          Username:
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>
        <button type="submit">Create User</button>
        </form>
    </div>
);
};
export default UserSignUp;
