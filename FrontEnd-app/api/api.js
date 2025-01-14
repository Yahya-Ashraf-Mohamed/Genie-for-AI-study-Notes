import axios from "axios";

// Set the base URL for the backend API
const API_BASE_URL ="http://localhost:8000";

// Create a reusable Axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
