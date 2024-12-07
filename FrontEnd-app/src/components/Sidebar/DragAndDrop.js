import React from "react";
import '../../styles/Sidebar/DragAndDrop.css'; 

const DragAndDrop = () => {
    return (
      <div className="drag-drop-container">
        {/* Drag and Drop Section */}
        <div className="drag-drop">
          <div className="drag-header">
            <button className="cancel-btn">Cancel</button>
            <button className="save-btn">Save</button>
          </div>
          <div className="drag-area">
            <p className="drag-text">Drag & Drop Files Here</p>
            <p className="or-text">or</p>
            <div className="button-container">
              <button className="browse-btn">Browse PC</button>
              <button className="browse-btn">Browse Drive</button>
            </div>
          </div>
        </div>
     </div>
    );
};

export default DragAndDrop;
