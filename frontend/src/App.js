import React, { useState } from 'react';
import PaymentEntry from './PaymentEntry';
import PaymentEntriesList from './PaymentEntriesList';
import SignUp from './SignUp';
import Login from './Login';
import './styles.css';

function App() {
  const [currentPage, setCurrentPage] = useState('SignUp');
  const userId = localStorage.getItem('user_id');
  return (
    <div id="app-container">
      <nav className="navbar">
        <div className="navbar-title">BUDGET BUDDY</div>
        <button onClick={() => setCurrentPage('Login')}>Login</button>
        <button onClick={() => setCurrentPage('SignUp')}>Sign Up</button>
        <button onClick={() => setCurrentPage('PaymentEntries')}>Payment Entries</button>
        <button onClick={() => setCurrentPage('PaymentEntriesList')}>Payment Entries List</button>
      </nav>
      <div className="main-content">
      {currentPage === 'Login' && <Login/>}
      {currentPage ==='SignUp' && <SignUp/>}
      {currentPage ==='PaymentEntries' && <PaymentEntry userId={userId} />}
      {currentPage ==='PaymentEntriesList' && <PaymentEntriesList userId={userId} />}
    </div>
    <footer className="footer">
      &copy; Budget Buddy by <a href="https://github.com/Linda-Njau" className="github-link">Linda-Njau</a>
    </footer>
    </div>
  );
}

export default App;
