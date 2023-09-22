import React, { useState } from 'react';
import { postData } from './httpService';
import DatePicker from 'react-datepicker'; 
import 'react-datepicker/dist/react-datepicker.css';
import PropTypes from 'prop-types';

const PaymentEntry = ({ user_id }) => {
    const [amount, setAmount ] = useState('');
    const [transactionDate, setTransactionDate] = useState(new Date());
    const [paymentCategory, setPaymentCategory] = useState('FOOD');

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log('Submit button clicked');
        try {
            const payload = { 
                amount: parseFloat(amount), 
                transactionDate: transactionDate.toISOString(),  
                paymentCategory: paymentCategory,
                user_id: user_id, //eslint-disable-line
            };
            const response = await postData('/payment_entries', payload);
            console.log('Payment Entry Sucess: ', response);
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
                  value={paymentCategory}
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
                  dateFormat="yyyy-dd-MM"
                />
            </label>
            <button type="submit">Submit</button>
        </form>
    );
    PaymentEntry.propTypes = {
        user_id: PropTypes.number.isRequired,
      };
};

export default PaymentEntry
