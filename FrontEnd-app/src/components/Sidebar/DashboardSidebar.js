import React from "react";
import '../../styles/Sidebar/Sidebar.css';
const Side = () => {
  const menuItems = [
    { name: "Home", icon: "🏠" },
    { name: "Dashboard", icon: "📊" },
    { name: "Library", icon: "📚" },
  ];

  const noteTakingItems = [
    { name: "My Notes" },
    { name: "Annotation" },
    { name: "Speech to Text" },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">Genie</div>
        <div className="hamburger-menu">☰</div>
      </div>
      <div className="sidebar-links">
        {menuItems.map((item, index) => (
          <a key={index} href={`#${item.name.toLowerCase()}`}>
            {item.icon} {item.name}
          </a>
        ))}

        <div className="expandable-section">
          <div className="expandable-header">
            Note Taking
            <span className="toggle-icon">▼</span>
          </div>
          <div className="expandable-links">
            {noteTakingItems.map((item, index) => (
              <a key={index} href={`#${item.name.toLowerCase()}`}>
                {item.name}
              </a>
            ))}
          </div>
        </div>
      </div>
      <div className="divider" />
      <div className="footer">
        <a href="#support">❓ Support</a>
        <a href="#settings">⚙️ Settings</a>
      </div>
    </aside>
  );
};

export default Side;
