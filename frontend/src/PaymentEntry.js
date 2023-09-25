import React, { useState } from 'react';
import { postData } from './httpService';
import DatePicker from 'react-datepicker'; 
import 'react-datepicker/dist/react-datepicker.css';
import PropTypes from 'prop-types';

const PaymentEntry = ({ userId }) => {
    const [amount, setAmount ] = useState('');
    const [transactionDate, setTransactionDate] = useState(new Date());
    const [payment_category, setPaymentCategory] = useState('FOOD');

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log('Submit button clicked');
        const formattedDate = transactionDate.toISOString().split('T')[0];
        console.log('Formatted Date:', formattedDate);
        try {
            const payload = { 
                amount: parseFloat(amount), 
                transactionDate: formattedDate,  
                payment_category: payment_category,
                user_id: userId,
            };
            console.log('Amount:', amount);
            console.log('Payment Category:', payment_category);
            console.log('the complete payload: ', payload)
            const response = await postData('/payment_entries', payload);
            console.log('Server Resonse: ', response);
            setAmount('');
            setTransactionDate(new Date());
        } catch (error) {
            console.error('Payment Entry Failed:', error);
        }
    };
    return (
            <div className="payment-form-container">
              <h2>Create Payment Entry</h2>
              <p>Recording every payment entry allows for more accurate results.</p>
              <img src="path/to/your/icon.png" alt="Description Icon" />
          
              <form className="payment-form" onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>
                    Amount:
                    <input type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    />
                  </label>
                  <small>Enter the amount you spent in numbers.</small>
                </div>
          
                <div className="form-group">
                  <label>
                    Payment Category:
                    <select value={payment_category} onChange={(e) => setPaymentCategory(e.target.value)}>
                      {/* ... options here ... */}
                    </select>
                  </label>
                  <small>Select the appropriate category for this payment.</small>
                </div>
          
                <div className="form-group">
                  <label>
                    Transaction Date:
                    <DatePicker
                      selected={transactionDate}
                      onChange={(date) => setTransactionDate(date)}
                      dateFormat="yyyy-MM-dd"
                    />
                  </label>
                  <small>Choose the date when the transaction was made.</small>
                </div>
          
                <button type="submit">Submit</button>
              </form>
            </div>
          );
          

    PaymentEntry.propTypes = {
        userId: PropTypes.number.isRequired,
      };
};

export default PaymentEntry
