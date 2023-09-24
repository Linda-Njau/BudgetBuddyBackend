import React, { useState } from 'react';
import PaymentEntry from './PaymentEntry';
import PaymentEntriesList from './PaymentEntriesList';
import UserSignUp from './UserSignUp';
import Login from './Login';
import './styles.css';

function App() {
  const [currentPage, setCurrentPage] = useState('SignUp');
  const userId = 1;
  return (
    <div className="App">
      <nav className="navbar">
        <img src={`${process.env.PUBLIC_URL}/logo.png`} alt="Logo" className="logo"/>
        <button onClick={() => setCurrentPage('Login')}>Login</button>
        <button onClick={() => setCurrentPage('SignUp')}>Sign Up</button>
        <button onClick={() => setCurrentPage('PaymentEntries')}>Payment Entries</button>
        <button onClick={() => setCurrentPage('PaymentEntriesList')}>Payment Entries List</button>
      </nav>
      <div className="content">
      {currentPage === 'Login' && <Login/>}
      {currentPage ==='SignUp' && <UserSignUp/>}
      {currentPage ==='PaymentEntries' && <PaymentEntry userId={userId} />}
      {currentPage ==='PaymentEntriesList' && <PaymentEntriesList userId={userId} />}
    </div>
    <footer className="footer">
      &copy; Budget Buddy by Linda Njau
    </footer>
    </div>
  );
}

export default App;
