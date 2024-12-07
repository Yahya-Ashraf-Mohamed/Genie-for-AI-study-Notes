// src/components/TabOptions.js
import React from 'react';
import '../styles/TabOptions.css';

const TabOptions = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { label: 'AI Summary', value: 'ai-summary' },
    { label: 'Generate Flashcards', value: 'flashcards' },
    { label: 'Generate Questions', value: 'questions' },
    { label: 'AI Annotation', value: 'annotation' },
  ];

  return (
    <div className="tab-options">
      {tabs.map((tab) => (
        <button
          key={tab.value}
          className={activeTab === tab.value ? 'active' : ''}
          onClick={() => setActiveTab(tab.value)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
};

export default TabOptions;
