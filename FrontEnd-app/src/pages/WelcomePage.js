// WelcomePage.js
import React from "react";
import { useNavigate } from "react-router-dom";
import '../styles/WelcomePage.css';  // For styling

const WelcomePage = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/login');  // Redirects to the login page
  };

  return (
    <div className="welcome-page">
      <div className="content">
        {/* Logo image from the public folder */}
        <img src="/Genie_Logo.png" alt="Logo" className="logo" />
        <p className="tagline">Your AI-powered study assistant</p>
        <button className="get-started-btn" onClick={handleGetStarted}>
          Get Started
        </button>
      </div>
    </div>
  );
};

export default WelcomePage;
