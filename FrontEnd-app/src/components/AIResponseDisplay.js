// src/components/AIResponseDisplay.js
import React from 'react';
import '../styles/AIResponseDisplay.css';

const AIResponseDisplay = ({ aiResponse, loading }) => {
  return (
    <div className="ai-response-display">
      {loading ? (
        <p>Loading AI response...</p>
      ) : aiResponse ? (
        <p>{aiResponse}</p>
      ) : (
        <p>Ask me anything, and I'll help!</p>
      )}
    </div>
  );
};

export default AIResponseDisplay;
