import React from "react";
import '../../styles/Sidebar/Footer.css';

const Footer = () => {
    return (
      <div className="footer-container">
        <div className="user-info">
          <div className="user-avatar">
            <span className="avatar-placeholder">👤</span>
          </div>
          <div className="user-details">
            <p className="user-name">Mariam</p>
            <p className="user-email">admin@gmail.com</p>
          </div>
          <button className="more-options">•••</button>
        </div>
      </div>
    );
  };
  
  export default Footer;