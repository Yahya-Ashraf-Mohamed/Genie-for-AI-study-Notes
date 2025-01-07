// App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import ForgetPasswordPage from "./pages/ForgetPasswordPage";
import ChatPage from "./pages/ChatPage"; 
import Dashboard from "./pages/DashboardPage"

const App = () => {
  // // State to hold the fetched message
  // const [data, setData] = useState("");

  // // Fetch data from FastAPI when the app loads
  // useEffect(() => {
  //   axios
  //     .get(`${process.env.REACT_APP_API_URL}/api`)
  //     .then((response) => {
  //       setData(response.data.message);
  //     })
  //     .catch((error) => {
  //       console.error("Error fetching data:", error);
  //     });
  // }, []);

  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<WelcomePage />} /> */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/forget-password" element={<ForgetPasswordPage />} />
        {/* Define route for the dashboard */}
        <Route path="/" element={<Dashboard />} />

        {/* Define route for the chat page */}
        <Route path="/chat/:fileName" element={<ChatPage />} />    


      </Routes>

      {/* <div>
        <h1>{data}</h1>
      </div> */}
    </Router>
  );
};

export default App;
