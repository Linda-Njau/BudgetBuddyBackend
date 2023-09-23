import React, { useState } from 'react';
import PaymentEntry from './PaymentEntry';
import PaymentEntriesList from './PaymentEntriesList';
import UserSignUp from './UserSignUp';
import Login from './Login';

function App() {
  const [currentPage, setCurrentPage] = useState('SignUp');
  const userId = 1;
  return (
    <div className="App">
      <h1>Budget Buddy</h1>
      <div>
        <button onClick={() => setCurrentPage('Login')}>Login</button>
        <button onClick={() => setCurrentPage('SignUp')}>Sign Up</button>
        <button onClick={() => setCurrentPage('PaymentEntries')}>Payment Entries</button>
        <button onClick={() => setCurrentPage('PaymentEntriesList')}>Payment Entries List</button>
      </div>
      {currentPage === 'Login' && <Login/>}
      {currentPage ==='SignUp' && <UserSignUp/>}
      {currentPage ==='PaymentEntries' && <PaymentEntry userId={userId} />}
      {currentPage ==='PaymentEntriesList' && <PaymentEntriesList userId={userId} />}
    </div>
  );
}

export default App;
