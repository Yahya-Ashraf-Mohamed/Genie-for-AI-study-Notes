import React from 'react';
import Sidebar from '../components/Sidebar/Sidebar';  
import MainContent from '../components/ChatMainContent';

const ChatPage = () => {
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <MainContent />
    </div>
  );
};

export default ChatPage;
