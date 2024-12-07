// src/components/MainContent.js
import React, { useState, useCallback } from 'react';
import '../styles/MainContent.css';
import AIResponseDisplay from './AIResponseDisplay';
import PromptInput from './PromptInput';

const MainContent = () => {
  const [input, setInput] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState(null); // No tab selected by default
  const [advancedOptions, setAdvancedOptions] = useState({
    type: 'MCQ',
    level: 'Easy',
  });

  const onInputChange = (e) => {
    setInput(e.target.value);
  };

  const onSubmit = useCallback(async (input) => {
    setLoading(true);
    setInput('');
    // Simulate an API call
    setTimeout(() => {
      setAiResponse(`AI response to: ${input}`);
      setLoading(false);
    }, 1000); // Simulate a delay
  }, []);

  const onGenerateClick = () => {
    if (activeTab === null) {
      alert('Please select a tab before generating.');
      return;
    }
    alert(`Generating ${activeTab} content with options: ${JSON.stringify(advancedOptions)}`);
    // Handle the actual generation logic here
  };

  const handleBoxClick = (tab) => {
    setActiveTab(tab);
  };

  return (
    <main className="main-content">
      <div className="content">
        {/* Move AIResponseDisplay to the top */}
        <AIResponseDisplay aiResponse={aiResponse} loading={loading} />

        <h1>How can I help you today?</h1>

        <PromptInput input={input} onInputChange={onInputChange} onSubmit={onSubmit} />

        {/* Big Gray Box for All Action Buttons */}
        <div className="action-buttons-container">
          {['AI Summary', 'Generate Flashcards', 'Generate Questions', 'AI Annotation'].map((tab) => (
            <div
              key={tab}
              className={`action-box ${activeTab === tab ? 'active' : ''}`}
              onClick={() => handleBoxClick(tab)}
            >
              <img src="/path/to/logo.png" alt="Logo" className="action-logo" />
              <span>{tab}</span>

              {/* Show dropdowns to the right of the button */}
              {activeTab === tab && (
                <div className="dropdown-container">
                  <div className="dropdown-label">Type</div>
                  <select
                    value={advancedOptions.type}
                    onChange={(e) => setAdvancedOptions({ ...advancedOptions, type: e.target.value })}
                    className="dropdown"
                  >
                    <option value="MCQ">MCQ</option>
                    <option value="Short Answer">Short Answer</option>
                  </select>

                  <div className="dropdown-label">Level</div>
                  <select
                    value={advancedOptions.level}
                    onChange={(e) => setAdvancedOptions({ ...advancedOptions, level: e.target.value })}
                    className="dropdown"
                  >
                    <option value="Easy">Easy</option>
                    <option value="Medium">Medium</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="action-buttons-footer">
          <button
            onClick={onGenerateClick}
            className="generate-button"
            disabled={!advancedOptions.type || !advancedOptions.level}
          >
            Generate
          </button>
        </div>
      </div>
    </main>
  );
};

export default MainContent;
