import axios from 'axios';

const httpClient = axios.create({
    baseURL: 'http://localhost:5000/',
});

httpClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers['Authorization'] = 'Bearer ' + token;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export const postData = async (endpoint, data) => {
    try {
        console.log('POST Data:', data);
        const response = await httpClient.post(endpoint, data);
        return response.data;
    } catch(error) {
        throw error;
    }
};
export const fetchPaymentEntries = async (user_id, payment_category, month) => {
    try {
        const endpoint = `/users/${user_id}/payment_entries`;
        const queryParams = new URLSearchParams();

        if (payment_category) {
            queryParams.append('payment_category', payment_category);
        }
        if (month) {
            queryParams.append('month', month);
        }
        if (queryParams.toString()) {
            endpoint += `?${queryParams.toString()}`;
        }
        const response = await httpClient.get(endpoint);
        return response.data;
    } catch (error) {
        throw error;
    }
};
