import axios from 'axios';

const httpClient = axios.create({
    baseURL: 'http://localhost:5000/',
});

export const postData = async (endpoint, data) => {
    try {
        const response = await httpClient.post(endpoint, data);
        return response.data;
    } catch(error) {
        throw error;
    }
};
