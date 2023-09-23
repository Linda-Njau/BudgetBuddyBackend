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
        <form onSubmit={handleSubmit}>
            <label>
                Amount:
                <input type="number"
                value={amount}
                onChange={(e) =>setAmount(e.target.value)}
                />
            </label>
            <label>
                Payment Category:
                <select
                  value={payment_category}
                  onChange={(e) => setPaymentCategory(e.target.value)}
                >
                    <option value="FOOD">FOOD</option>
                    <option value="TRAVEL">TRAVEL</option>
                    <option value="UTILITIES">UTILITIES</option>
                    <option value="TRANSPORTATION">TRANSPORT</option>
                    <option value="ENTERTAINMENT">ENTERTAINMENT</option>
                  </select>
            </label>
            <label>
                Transaction Date:
                <DatePicker
                  selected={transactionDate}
                  onChange={(date) => setTransactionDate(date)}
                  dateFormat="yyyy-MM-dd"
                />
            </label>
            <button type="submit">Submit</button>
        </form>
    );
    PaymentEntry.propTypes = {
        userId: PropTypes.number.isRequired,
      };
};

export default PaymentEntry
