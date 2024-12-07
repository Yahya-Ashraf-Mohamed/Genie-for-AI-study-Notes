// src/components/PromptInput.js
import React, { useCallback } from 'react';
import '../styles/PromptInput.css';

const PromptInput = ({ input, onInputChange, onSubmit }) => {
  const handleSubmit = useCallback(() => {
    if (input.trim()) {
      onSubmit(input);  // Only submit if input is not empty
    }
  }, [input, onSubmit]);

  return (
    <div className="prompt-input">
      <input
        type="text"
        value={input}
        onChange={onInputChange}
        className="input-box"
        placeholder="Enter your prompt here"
      />
      <button onClick={handleSubmit} className="submit-button" disabled={!input.trim()}>
        <span className="material-icons">send</span>
      </button>
    </div>
  );
};

export default PromptInput;
