import React, { useState, useEffect } from 'react';
import { Card } from 'react-bootstrap';

function NewsSpace({ activeNewsData }) {
  const [newsSummaries, setNewsSummaries] = useState([]);

  useEffect(() => {
    if (activeNewsData?.ui_type === 'news_feed') {
      console.log('Active News Data:', activeNewsData.ui_content); // Debug log
      setNewsSummaries(activeNewsData.ui_content); 
    }
  }, [activeNewsData]);

  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    minHeight: 0,
  };

  const headerStyle = {
    padding: '1rem',
    borderBottom: '1px solid #dee2e6',
    backgroundColor: 'white',
  };

  const contentStyle = {
    flex: 1,
    overflowY: 'auto',
    padding: '1rem',
    minHeight: 0,
  };

  return (
    <div style={containerStyle}>
      <div style={headerStyle}>
        <h4 className="m-0">Latest News Summaries</h4>
      </div>
      
      <div style={contentStyle}>
        {newsSummaries.length > 0 ? (
          newsSummaries.map((news, index) => (
            <Card key={index} className="mb-3">
              <Card.Body>
                <Card.Title>{news.title}</Card.Title>
                <Card.Text>{news.summary}</Card.Text>
                <Card.Footer className="text-muted">
                  {news.timestamp} • {news.source}
                  {news.url && (
                    <div>
                      <a href={news.url} target="_blank" rel="noopener noreferrer">
                        Read Full Article
                      </a>
                    </div>
                  )}
                </Card.Footer>
              </Card.Body>
            </Card>
          ))
        ) : (
          <p>No news summaries available. Trigger a news request from the chat.</p>
        )}
      </div>
    </div>
  );
}

export default NewsSpace;
