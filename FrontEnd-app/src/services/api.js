import axios from "axios";

// Base URL from .env
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// Sign-up API function
export const createUser = async (email, password) => {
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
  try {
    const response = await axios.post(`${API_URL}/user`, {
      email,
      password,
    });
    return response.data;
  } catch (error) {
    console.error("Error creating user:", error.response?.data || error);
    throw error;
  }
};