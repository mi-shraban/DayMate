import React, { useState, useEffect } from 'react';
import { fetchDailyPlan } from '../services/api';
import WeatherDisplay from '../components/WeatherDisplay';
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
        setDailyPlan(data);
      } catch (err) {
        setError('Failed to load daily plan. Please try again later.');
        console.error(err); // Log for debugging
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
          <NewsDisplay newsData={dailyPlan.news} />
          <Recommendations recommendations={dailyPlan.recommendations} />
        </>
      )}
    </div>
  );
};

export default Dashboard;