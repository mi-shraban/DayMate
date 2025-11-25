import React from 'react';

const WeatherDisplay = ({ weatherData }) => {
  if (!weatherData || !weatherData.main) return <p>Loading weather...</p>;

  return (
    <div className="weather-card">
      <h3>Current Weather</h3>
      <p>Location: {weatherData.name}, {weatherData.sys?.country}</p>
      <p>Temperature: {weatherData.main.temp} °C</p>
      <p>Description: {weatherData.weather[0]?.description}</p>
      <p>Humidity: {weatherData.main.humidity}%</p>
    </div>
  );
};

export default WeatherDisplay;