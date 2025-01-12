import React, { useState, useEffect } from "react";
import axios from "axios";
import '../styles/DashboardMainContent.css';
import { useNavigate } from "react-router-dom";

const API_BASE_URL = " http://127.0.0.1:8000"; // Base API URL

const DashboardMainContent = () => {
  // State to store the list of uploaded files
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [fileToUpload, setFileToUpload] = useState(null); // State for the file to be uploaded
  const navigate = useNavigate(); // React Router's navigation hook

  // Fetch the list of uploaded files from the API
  const fetchUploadedFiles = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/home`);
      console.log(response.data.files);
      setUploadedFiles(response.data.files); // Update the state with fetched files
    } catch (error) {
      console.error('Error fetching uploaded files:', error);
    }
  };

  // Handle file upload
  const handleFileChange = (event) => {
    setFileToUpload(event.target.files[0]); // Save the selected file to state
  };

  const handleFileUpload = async () => {
    if (!fileToUpload) {
      console.error("No file selected.");
      return; // Do nothing if no file is selected
    }
  
    const formData = new FormData();
    formData.append("file", fileToUpload); 
  
    try {
      // Send the file to the server
      const response = await axios.post(`${API_BASE_URL}/uploadfile`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
  
      // Check if the response was successful
      if (response.status === 200) {
        console.log("File uploaded successfully:", response.data);
        
        // Fetch the updated list of files after uploading
        fetchUploadedFiles();
  
        // Reset the file input and file state
        setFileToUpload(null);
      } else {
        console.error("File upload failed", response);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("There was an error uploading the file. Please try again.");
    }
  };
  
  
  // Handle actions for Chat, Summary, and Quiz buttons
  const handleChat = async (fileName) => {
    console.log(`Requesting model preparation for ${fileName}`);

    try {
        // Send an API request with query parameters
        const response = await fetch(`${API_BASE_URL}/newchat?material_path=${encodeURIComponent(fileName)}`, {
            method: 'POST',
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to prepare model instance');
        }

        const data = await response.json();
        console.log(data.message); // Log success message
    } catch (error) {
        console.error('Error during model preparation request:', error.message);
    }
    navigate(`/chat/${fileName}`); // Navigate to the chat page with the file name

};



  const handleSummary = (fileName) => {
    console.log(`Summary action triggered for ${fileName}`);
    // Add logic for generating a summary of the file
  };


  const handleQuiz = (fileName) => {
    console.log(`Quiz action triggered for ${fileName}`);
    // Add logic for generating a quiz from the file content
  };
  

  // Fetch files when the component is mounted
  useEffect(() => {
    fetchUploadedFiles();
  }, []); // Empty dependency array ensures this runs only once after the initial render




  return (
    <main className="main-content">
      <div className="content">
        <h1>Dashboard</h1>

        {/* File Upload Input */}
        <div className="file-upload-section">
          <input
            type="file"
            onChange={handleFileChange} // Handle file selection
            className="file-upload-input"
          />
          <button onClick={handleFileUpload} className="upload-btn">
            Upload File
          </button>
        </div>

        {/* Display uploaded files as a list */}
        <div className="uploaded-files-section">
          <h3>Uploaded Files:</h3>
          {uploadedFiles.length === 0 ? (
            <p>No files uploaded yet.</p>
          ) : (
            <ul className="uploaded-files-list">
              {uploadedFiles.length === 0 ? (
                <p>No files uploaded yet.</p>
              ) : (
                uploadedFiles.map((file, index) => (
                  <li key={index} className="uploaded-file-item">
                    <span>{file}</span>  {/* Display the file name here */}
                    <div className="file-actions">
                     
                    <button onClick={() => handleChat(file)} className="action-btn chat-btn">
                      Chat
                    </button>

                    <button onClick={() => handleSummary(file)} className="action-btn summary-btn">
                      Summary
                    </button>
                    
                    <button onClick={() => handleQuiz(file)} className="action-btn quiz-btn">
                      Quiz
                    </button>
                  
                  </div>
                  
                  </li>
                ))
              )}
            </ul>

          )}
        </div>
      </div>
    </main>
  );
};

export default DashboardMainContent;
