import React from 'react';

const Recommendations = ({ recommendations }) => {
  return (
    <div className="recommendations-card">
      <h3>DayMate's Suggestions</h3>
      {recommendations ? (
        <p>{recommendations}</p>
      ) : (
        <p>Loading suggestions...</p>
      )}
    </div>
  );
};

export default Recommendations;