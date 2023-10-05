import React, { useState, useEffect } from 'react';
import { fetchPaymentEntries } from './httpService';
import './styles.css';
import withAuth from './withAuth';

const PaymentEntriesList = ({ userId }) => {
  console.log('PaymentEntriesList component mounted');
  const [allPaymentEntries, setAllPaymentEntries] = useState([]);
  const [filteredPaymentEntries, setFilteredPaymentEntries] = useState([]);
  const [paymentCategory, setPaymentCategory] = useState('');
  const [month, setMonth] = useState('');

  // Define the filterEntries function within the component
  const filterEntries = () => {
    console.log('Filtering payment entries...');
    console.log('Payment Category:', paymentCategory);
    console.log('Month:', month);
    const filteredEntries = allPaymentEntries.filter((entry) => {
      // Check if entry.paymentCategory and entry.transactionDate exist before using includes
      const matchesCategory =
        entry.payment_category && entry.payment_category.includes(paymentCategory);
      let matchesMonth = false;
      if (entry.transaction_date) {
        const date = new Date(entry.transaction_date);
        const entryMonth = date.getMonth() + 1;
        const formattedEntryMonth = String(entryMonth).padStart(2, '0');
        matchesMonth = formattedEntryMonth === month;
      }
      console.log('Matches Category:', matchesCategory);
      console.log('Matches Month:', matchesMonth);
      return (matchesCategory || !paymentCategory) && (matchesMonth || !month);
    });

    console.log('Filtered Entries after filter:', filteredEntries);
    setFilteredPaymentEntries(filteredEntries);
  };
  const handleReset = async () => {
    try {
      // Fetch all payment entries without filters
      const entries = await fetchPaymentEntries(userId, '', '');
      setAllPaymentEntries(entries);
      setFilteredPaymentEntries([]); // Clear filtered entries
    } catch (error) {
      console.error('Error resetting payment entries', error);
    }
  };

  useEffect(() => {
    // Fetch all payment entries without filters when the component mounts
    const fetchEntries = async () => {
      try {
        const entries = await fetchPaymentEntries(userId, '', '');
        setAllPaymentEntries(entries);
        console.log('API Response fetch all entries:', entries);
      } catch (error) {
        console.error('Error fetching payment entries', error);
      }
    };
    fetchEntries();
  }, [userId]);

  // Apply filters whenever paymentCategory or month change
  useEffect(() => {
    filterEntries();
  }, [paymentCategory, month, allPaymentEntries]);
  
  return (
    <div className="filter-container">
      <h2>Your Payment Entries</h2>
      <div className="filter-group">
        <div className="filter-item">
        <label>
          Payment Category:
          <input
            type="text"
            value={paymentCategory}
            onChange={(e) => {
              console.log('Payment Category Changed:', e.target.value);
              setPaymentCategory(e.target.value);
            }}
          />
        </label>
      </div>
      <div className="filter-item">
        <label>
          Month:          
          <input
            type="text"
            value={month}
            onChange={(e) => {
              console.log('Month Changed:', e.target.value);
              setMonth(e.target.value);
            }}
          />
        </label>
      </div>
        <button className="filter-button" onClick={filterEntries}>
          Filter
        </button>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th>Amount</th>
            <th>Category</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {filteredPaymentEntries.map((entry, index) => (
            <tr key={entry.id}>
              <td>{entry.amount}</td>
              <td>{entry.payment_category}</td>
              <td>{entry.transaction_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PaymentEntriesList;
