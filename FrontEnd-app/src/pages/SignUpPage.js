import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createUser } from "../services/api";  // Import API function
import '../styles/SignUpPage.css';

const SignUpPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSignUp = async (e) => {
    e.preventDefault();  // Prevent form reload

    try {
      // Call the back-end to create the user
      const result = await createUser(email, password);
      console.log("Sign-up successful!", result);

      // Redirect to home on success
      navigate("/");
    } catch (err) {
      setError("Sign-up failed. Please try again.");
    }
  };

  return (
    <div className="signup-page">
      <div className="form-container">
        <h1 className="signup-title">Sign Up</h1>
        <form onSubmit={handleSignUp} className="signup-form">
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

          <button type="submit" className="signup-btn">Sign Up</button>
        </form>

        {error && <p className="error-message">{error}</p>}  {/* Show error if exists */}

        <div className="login-link">
          <p>Already have an account? <a href="/login">Login</a></p>
        </div>
      </div>
    </div>
  );
};

export default SignUpPage;
