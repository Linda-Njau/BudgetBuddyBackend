import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const withAuth = (ComponentToProtect) => {
  return (props) => {
    const navigate = useNavigate();
    const token = localStorage.getItem('token');

    useEffect(() => {
        if (!token) {
          navigate('/login'); // Navigate to the login page
        }
      }, [token, navigate]);
  
      if (token) {
        return <ComponentToProtect {...props} />;
      } else {
        return null;  // Or some placeholder
      }
    };
  };
  
  export default withAuth;
