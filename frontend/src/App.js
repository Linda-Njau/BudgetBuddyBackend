import React from 'react';
import PaymentEntry from './PaymentEntry';
import PaymentEntriesList from './PaymentEntriesList';
import UserCreation from './UserCreation';

function App() {
  const user_id = 1;
  return (
    <div className="App">
      <h1>Budget Buddy</h1>
      <UserCreation/>
      <PaymentEntry user_id={user_id}/>
      <PaymentEntriesList user_id={user_id} />
    </div>
  );
}

export default App;
