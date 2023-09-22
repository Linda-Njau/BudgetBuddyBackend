import React, { useState, useEffect } from 'react';
import { fetchPaymentEntries } from './httpService';

const PaymentEntriesList = ({ user_id }) => {
  console.log('PaymentEntriesList component mounted');
  const [allPaymentEntries, setAllPaymentEntries] = useState([]);
  const [filteredPaymentEntries, setFilteredPaymentEntries] = useState([]);
  const [paymentCategory, setPaymentCategory] = useState('');
  const [month, setMonth] = useState('');

  useEffect(() => {
    // Fetch all payment entries without filters when component mounts
    const fetchEntries = async () => {
      try {
        const entries = await fetchPaymentEntries(user_id, '', '');
        setAllPaymentEntries(entries);
        console.log('API Response fetch all entries:', entries);
      } catch (error) {
        console.error('Error fetching payment entries', error);
      }
    };
    fetchEntries();
  }, [user_id]);

  useEffect(() => {
    // Function to filter payment entries based on paymentCategory and month
    const filterEntries = () => {
      console.log('Filtering payment entries...');
      console.log('Payment Category:', paymentCategory);
      console.log('Month:', month);
      const filteredEntries = allPaymentEntries.filter((entry) => {
        // Check if entry.paymentCategory and entry.transactionDate exist before using includes
        const matchesCategory =
          entry.payment_category && entry.payment_category.includes(paymentCategory);
        const matchesMonth =
          entry.transaction_date && entry.transaction_date.includes(month);
        console.log('Matches Category:', matchesCategory);
        console.log('Matches Month:', matchesMonth);
          return (matchesCategory || !paymentCategory) && (matchesMonth || !month);
      });
      
      console.log('Filtered Entries after filter:', filteredEntries);
      setFilteredPaymentEntries(filteredEntries);
    };

    // Apply filters whenever paymentCategory or month change
    filterEntries();
  }, [paymentCategory, month, allPaymentEntries]);

  return (
    <div>
      <h2>Your Payment Entries</h2>
      <div>
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
        <button onClick={() => setFilteredPaymentEntries([...allPaymentEntries])}>
          Filter
        </button>
      </div>
      <table>
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


