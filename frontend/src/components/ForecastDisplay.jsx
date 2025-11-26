// frontend/src/components/ForecastDisplay.jsx
import React from 'react';

const ForecastDisplay = ({ forecastData }) => {
  console.log('ForecastDisplay received:', forecastData);

  if (!forecastData || !forecastData.type) {
    return (
      <div className="forecast-card">
        <h3>Forecast</h3>
        <p>Loading forecast data...</p>
      </div>
    );
  }

  const formatTime = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    });
  };

  // Hourly forecast (One Call API)
  if (forecastData.type === 'hourly' && forecastData.hourly?.length > 0) {
    const next12Hours = forecastData.hourly.slice(0, 12);

    return (
      <div className="forecast-card">
        <h3>Hourly Forecast (Next 12 Hours)</h3>
        <div style={{ overflowX: 'auto' }}>
          <div style={{ display: 'flex', gap: '15px', padding: '10px 0' }}>
            {next12Hours.map((hour, index) => (
              <div
                key={index}
                style={{
                  minWidth: '100px',
                  textAlign: 'center',
                  padding: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '8px',
                  backgroundColor: '#f9f9f9'
                }}
              >
                <div style={{ fontWeight: 'bold' }}>{formatTime(hour.dt)}</div>
                <div style={{ fontSize: '24px', margin: '10px 0' }}>
                  {Math.round(hour.temp)}°C
                </div>
                <div style={{ fontSize: '12px', color: '#666' }}>
                  {hour.weather[0].description}
                </div>
                <div style={{ fontSize: '12px', color: '#999', marginTop: '5px' }}>
                  💧 {hour.humidity}%
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // 3-hour forecast (Free tier)
  if (forecastData.type === '3-hour' && forecastData.list?.length > 0) {
    const next24Hours = forecastData.list.slice(0, 8); // 8 * 3 hours = 24 hours

    return (
      <div className="forecast-card">
        <h3>Weather Forecast (Next 24 Hours)</h3>
        <div style={{ overflowX: 'auto' }}>
          <div style={{ display: 'flex', gap: '15px', padding: '10px 0' }}>
            {next24Hours.map((item, index) => (
              <div
                key={index}
                style={{
                  minWidth: '110px',
                  textAlign: 'center',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '8px',
                  backgroundColor: '#f9f9f9'
                }}
              >
                <div style={{ fontWeight: 'bold', fontSize: '12px' }}>
                  {formatDate(item.dt)}
                </div>
                <div style={{ fontSize: '11px', color: '#666' }}>
                  {formatTime(item.dt)}
                </div>
                <div style={{ fontSize: '28px', margin: '10px 0', fontWeight: 'bold' }}>
                  {Math.round(item.main.temp)}°C
                </div>
                <div style={{ fontSize: '12px', color: '#666', textTransform: 'capitalize' }}>
                  {item.weather[0].description}
                </div>
                <div style={{ fontSize: '11px', color: '#999', marginTop: '5px' }}>
                  💧 {item.main.humidity}%
                </div>
                {item.rain && (
                  <div style={{ fontSize: '11px', color: '#4a90e2', marginTop: '3px' }}>
                    🌧️ {item.rain['3h']}mm
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="forecast-card">
      <h3>Forecast</h3>
      <p>Forecast type: {forecastData.type}</p>
      <p>No forecast data available. Check console for details.</p>
    </div>
  );
};

export default ForecastDisplay;