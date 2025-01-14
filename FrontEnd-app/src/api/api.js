import axios from "axios";

// Static backend API URL
const API_BASE_URL = "http://localhost:5000"; // Replace with your backend URL

// Create Axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
