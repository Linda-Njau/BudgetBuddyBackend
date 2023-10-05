import React from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutButton = ({setToken, setUserId}) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Remove the access token and user ID from localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');

    setToken(null);
    setUserId(null);
    // Redirect the user to the login page
    navigate('/'); // Replace '/login' with the path to your Login component
  };

  return (
    <button onClick={handleLogout}>Logout</button>
  );
};

export default LogoutButton;
