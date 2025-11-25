import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Change if your backend runs elsewhere

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

export const fetchDailyPlan = async () => {
  try {
    const response = await apiClient.get('/api/v1/planning/daily-plan');
    return response.data;
  } catch (error) {
    console.error('Error fetching daily plan:', error);
    throw error; // Re-throw to handle in component
  }
};