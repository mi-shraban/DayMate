import React, { useState, useEffect } from 'react';
import { fetchDailyPlan } from '../services/api';
import WeatherDisplay from '../components/WeatherDisplay';
import ForecastDisplay from '../components/ForecastDisplay';
import NewsDisplay from '../components/NewsDisplay';
import Recommendations from '../components/Recommendations';

const Dashboard = () => {
  const [dailyPlan, setDailyPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadPlan = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchDailyPlan();
        console.log('Received daily plan:', data);
        console.log('Forecast data:', data.forecast);
        setDailyPlan(data);
      } catch (err) {
        setError('Failed to load daily plan. Please try again later.');
        console.error('Error loading plan:', err);
      } finally {
        setLoading(false);
      }
    };

    loadPlan();
  }, []);

  if (loading) return <div className="loading">Loading your daily plan...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="dashboard">
      <h1>DayMate - Your AI Daily Planner</h1>
      {dailyPlan && (
        <>
          <WeatherDisplay weatherData={dailyPlan.weather} />
          <ForecastDisplay forecastData={dailyPlan.forecast} />
          <NewsDisplay newsData={dailyPlan.news} />
          <Recommendations recommendations={dailyPlan.recommendations} />
        </>
      )}
    </div>
  );
};

export default Dashboard;