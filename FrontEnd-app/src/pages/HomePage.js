import React from 'react';
import Sidebar from '../components/Sidebar/Sidebar';  
import MainContent from '../components/MainContent';

const HomePage = () => {
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <MainContent />
    </div>
  );
};

export default HomePage;
