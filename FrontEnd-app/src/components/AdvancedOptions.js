// src/components/AdvancedOptions.js
import React, { useEffect, useState } from 'react';
import '../styles/AdvancedOptions.css';

const AdvancedOptions = ({ activeTab, advancedOptions, setAdvancedOptions }) => {
  const [type, setType] = useState(advancedOptions.type);
  const [level, setLevel] = useState(advancedOptions.level);

  useEffect(() => {
    // Reset advanced options when tab changes
    setType(advancedOptions.type);
    setLevel(advancedOptions.level);
  }, [activeTab, advancedOptions]);

  const handleTypeChange = (e) => {
    setType(e.target.value);
    setAdvancedOptions((prev) => ({ ...prev, type: e.target.value }));
  };

  const handleLevelChange = (e) => {
    setLevel(e.target.value);
    setAdvancedOptions((prev) => ({ ...prev, level: e.target.value }));
  };

  return (
    <div className="advanced-options">
      <div>
        <label>Type</label>
        <select value={type} onChange={handleTypeChange}>
          <option>MCQ</option>
          <option>Essay Questions</option>
          <option>Short Answer</option>
        </select>
      </div>
      <div>
        <label>Level</label>
        <select value={level} onChange={handleLevelChange}>
          <option>Easy</option>
          <option>Moderate</option>
          <option>Hard</option>
        </select>
      </div>
    </div>
  );
};

export default AdvancedOptions;
