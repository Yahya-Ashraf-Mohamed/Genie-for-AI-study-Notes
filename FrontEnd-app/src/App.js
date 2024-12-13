// App.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import WelcomePage from "./pages/WelcomePage";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import ForgetPasswordPage from "./pages/ForgetPasswordPage";
import HomePage from "./pages/HomePage";  // Import HomePage

const App = () => {
  // State to hold the fetched message
  const [data, setData] = useState("");

  // Fetch data from FastAPI when the app loads
  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_URL}/api`)
      .then((response) => {
        setData(response.data.message);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<WelcomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/forget-password" element={<ForgetPasswordPage />} />
        <Route path="/home" element={<HomePage />} /> {/* Add home route */}
      </Routes>

      {/* Display the fetched message */}
      <div>
        <h1>{data}</h1>
      </div>
    </Router>
  );
};

export default App;
