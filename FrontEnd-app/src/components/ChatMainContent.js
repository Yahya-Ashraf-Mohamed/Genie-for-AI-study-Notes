import React, { useState } from "react";
import { useParams } from "react-router-dom";
import '../styles/ChatMainContent.css';
import PromptInput from './PromptInput';
import ReactMarkdown from "react-markdown"; 
import apiClient from "../api/api"; // Import the centralized API client


const ChatMainContent = () => {
  const { fileName } = useParams(); // Get the file name from the route parameter
  const [input, setInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const onInputChange = (e) => {
    setInput(e.target.value);
  };

const askRagModel = async (question) => {
  try {
    // Use query parameters instead of the POST body
    const response = await apiClient.post("/ask_rag_model", null, {
      params: { question }, // Send question as a query parameter
    });

    return response.data.answer; // Assuming the backend returns { answer: "..." }
  } catch (error) {
    const errorMessage =
      error.response?.data?.detail || "Failed to get a response from the RAG model.";
    console.error("Error while querying the RAG model:", errorMessage);
    throw new Error(errorMessage);
  }
};


 
  const onSubmit = async (input) => {
    if (!input.trim()) return;
    setLoading(true);

    setChatHistory((prevHistory) => [
      ...prevHistory,
      { sender: "User", message: input },
    ]);

    setInput('');

    try {
      const response = await askRagModel(input);
      setChatHistory((prevHistory) => [
        ...prevHistory,
        { sender: "AI", message: response },
      ]);
    } catch (error) {
      setChatHistory((prevHistory) => [
        ...prevHistory,
        { sender: "AI", message: `Error: ${error.message}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="main-content">
      <h1 className="chat-header">Chat With {fileName}</h1>
      <div className="chat-box">
        <div className="chat-history">
          {chatHistory.map((chat, index) => (
            <div
              key={index}
              className={`chat-message ${
                chat.sender === "User" ? "user-message" : "ai-message"
              }`}
            >
              {/* Use ReactMarkdown to render the message */}
              <ReactMarkdown>{chat.message}</ReactMarkdown>
             </div>
          ))}
          {loading && <div className="chat-message ai-message">Typing...</div>}
        </div>
        <PromptInput
          input={input}
          onInputChange={onInputChange}
          onSubmit={onSubmit}
        />
      </div>
    </main>
  );
};

export default ChatMainContent;
