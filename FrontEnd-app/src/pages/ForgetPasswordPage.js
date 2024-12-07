// ForgetPasswordPage.js
import React, { useState } from "react";
import { Navigate } from "react-router-dom"; // Use Navigate component for redirect

const ForgetPasswordPage = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [isRedirected, setIsRedirected] = useState(false); // State to trigger redirection after form submission

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simulate password reset logic
    setMessage("If the email is registered, a reset link will be sent.");
    
    // Redirect to login page after a short delay
    setTimeout(() => {
      setIsRedirected(true);  // Trigger redirection
    }, 3000);
  };

  if (isRedirected) {
    // Redirect to the login page after the delay
    return <Navigate to="/login" />;
  }

  return (
    <div className="forget-password-page">
      <div className="form-container">
        <h1 className="title">Forget Password</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email">Enter your email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <button type="submit">Send Reset Link</button>
        </form>
        {message && <p>{message}</p>}
        <div>
          <p>Remembered your password? <a href="/login">Login here</a></p>
        </div>
      </div>
    </div>
  );
};

export default ForgetPasswordPage;
