import React, { useState } from "react";
import '../../styles/Sidebar/SidebarItem.css';
import expandIcon from '../../assets/icons/expand-icon.png';  // Make sure the path is correct
import collapseIcon from '../../assets/icons/collapse-icon.png';  // Make sure the path is correct

const SidebarItem = ({ name, icon, subItems }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSubItems = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div>
      <div onClick={toggleSubItems} className="sidebar-item">
        <span className="item-content">
          {icon && <span>{icon}</span>}
          <span>{name}</span>
        </span>
        {subItems && (
          <span>
            {isOpen ? (
              <img
                src={collapseIcon}
                alt="Collapse"
                className="toggle-icon"
              />
            ) : (
              <img
                src={expandIcon}
                alt="Expand"
                className="toggle-icon"
              />
            )}
          </span>
        )}
      </div>

      {isOpen && subItems && (
        <div className="sub-items">
          {subItems.map((subItem, index) => (
            <p key={index} className="sub-item">
              {subItem.name}
            </p>
          ))}
        </div>
      )}
    </div>
  );
};

export default SidebarItem;
