import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import PaymentEntry from './PaymentEntry';
import PaymentEntriesList from './PaymentEntriesList';
import SignUp from './SignUp';
import Login from './Login';
import LogoutButton from './LogoutButton';
import './styles.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [userId, setUserId] = useState(localStorage.getItem('user_id'));  

  useEffect(() => {
    const handleStorageChange = () => {
      setToken(localStorage.getItem('token'));
      setUserId(localStorage.getItem('user_id'));
    };

    // Listen to storage events
    window.addEventListener('storage', handleStorageChange);

    return () => {
      // Clean up the event listener
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  return (
    <Router>
      <div id="app-container">
        <nav className="navbar">
          <div className="navbar-title">BUDGET BUDDY</div>
          { token ? (
            // If user is authenticated
            <>
              <LogoutButton setToken={setToken} setUserId={setUserId}/>
              <Link to="/PaymentEntry">
                <button>Payment Entries</button>
              </Link>
              <Link to="/PaymentEntriesList">
                <button>Payment Entries List</button>
              </Link>
            </>
          ) : (
            // If user is not authenticated
            <>
              <Link to="/Login">
                <button>Login</button>
              </Link>
              <Link to="/SignUp">
                <button>Sign Up</button>
              </Link>
            </>
          )}
        </nav>
        <div className="main-content">
          <Routes>
            <Route path="/" element={<Login />} index />
            <Route path="/SignUp" element={<SignUp />} />
            <Route path="/PaymentEntry" element={<PaymentEntry userId={userId} />} />
            <Route path="/PaymentEntriesList" element={<PaymentEntriesList userId={userId} />} />
          </Routes>
        </div>
        <footer className="footer">
          &copy; Budget Buddy by <a href="https://github.com/Linda-Njau" className="github-link">Linda-Njau</a>
        </footer>
      </div>
    </Router>
  );  
}

export default App;
