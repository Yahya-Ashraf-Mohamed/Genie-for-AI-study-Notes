import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import '../styles/LoginPage.css';

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();  // Initialize navigate

  const handleLogin = (e) => {
    e.preventDefault();
    
    const testEmail = "admin@gmail.com";
    const testPassword = "admin@123";
    
    if (email === testEmail && password === testPassword) {
      console.log("Login successful!");
      navigate("/home");
    } else {
      console.log("Invalid email or password.");
    }
  };

  return (
    <div className="login-page">
      <div className="form-container">
        <h1 className="login-title">Login</h1>
        <form onSubmit={handleLogin} className="login-form">
          <div className="input-group">
            <label htmlFor="email" className="input-label">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              className="input-field"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          
          <div className="input-group">
            <label htmlFor="password" className="input-label">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              className="input-field"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="login-btn">Login</button>
        </form>
        
        <div className="signup-link">
          <p>Don't have an account? <a href="/signup">Sign up</a></p>
        </div>
        
        <div className="forgot-password-link">
          <p><a href="/forgot-password">Forgot password?</a></p>
        </div>
      </div>
    </div>
  );
};


export default LoginPage;
