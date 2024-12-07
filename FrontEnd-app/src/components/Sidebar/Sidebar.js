import React from "react";
import '../../styles/Sidebar/Sidebar.css'; 
import SidebarItem from "./SidebarItem";
import DragAndDrop from "./DragAndDrop";
import Footer from "./Footer"; 

const Sidebar = () => {
  // Main menu items
  const items = [
    { name: "Home", icon: "🏠" },
    { name: "Dashboard", icon: "📊" },
    { name: "Library", icon: "📚" },
  ];

  // Sub-items for the "Note Taking" section
  const noteSubItems = [
    { name: "My Notes" },
    { name: "Annotation" },
    { name: "Speech to Text" },
  ];

  return (
    <aside className="sidebar">
      <div className="logo">Genie</div>
      {/* Main navigation items */}
      <div>
        {items.map((item, index) => (
          <SidebarItem key={index} name={item.name} icon={item.icon} />
        ))}

        {/* Note Taking section with sub-items */}
        <div className="note-section">
          <SidebarItem name="Note Taking" subItems={noteSubItems} />
        </div>
      </div>

      {/* Divider */}
      <div className="divider" />

      {/* Drag and Drop section */}
      <DragAndDrop />

      {/* Divider */}
      <div className="divider" />

      {/* Support and Settings items */}
      <div className="support-settings-section">
        <SidebarItem name="Support" icon="❓" />
        <SidebarItem name="Settings" icon="⚙️" />
      </div>

      {/* Divider */}
      <div className="divider" />

      {/* User Info & Footer */}
      <Footer />
    </aside>
  );
};

export default Sidebar;

