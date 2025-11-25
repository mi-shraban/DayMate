import React from 'react';

const NewsDisplay = ({ newsData }) => {
  const articles = newsData?.articles || [];

  return (
    <div className="news-card">
      <h3>Local News</h3>
      {articles.length > 0 ? (
        <ul>
          {articles.map((article, index) => (
            <li key={index}>
              <a href={article.url} target="_blank" rel="noopener noreferrer">
                {article.title}
              </a>
            </li>
          ))}
        </ul>
      ) : (
        <p>Loading news...</p>
      )}
    </div>
  );
};

export default NewsDisplay;