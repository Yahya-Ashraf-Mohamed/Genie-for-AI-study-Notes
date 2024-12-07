import React, { useState } from 'react';
import './styles/file-upload.css';

const FileUpload = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  return (
    <div className="file-upload">
      <input type="file" onChange={handleFileChange} id="fileInput" hidden />
      <label htmlFor="fileInput" className="upload-box">
        {file ? file.name : "Drag & Drop Files Here or Browse"}
      </label>
      <div className="buttons">
        <button>Browse PC</button>
        <button>Browse Drive</button>
      </div>
    </div>
  );
};

export default FileUpload;
