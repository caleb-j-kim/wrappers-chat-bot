import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState(''); // State for the current message
  const [messages, setMessages] = useState([]); // State to store all sent messages

  // Function to handle sending a message
  const handleSend = () => {
    if (message.trim()) {
      // Add the current message to the list of messages
      setMessages([...messages, message]);
      setMessage(''); // Clear the text area after sending
    }
  };

  return (
    <div className="App">
      {/* Display the ACM Logo image at the top */}
      <img src="/acm-logo.png" alt="ACM Logo" className="header-image" />

      {/* Main content */}
      <h1>ACM Education Chat Bot</h1>

      {/* Display sent messages */}
      <div className="messages-container">
        {messages.map((msg, index) => (
          <div key={index} className="message animate-message">
            {msg}
          </div>
        ))}
      </div>

      {/* Chat input section */}
      <div className="chat-container">
        <textarea
          className="chat-input"
          placeholder="Type your message here..."
          value={message}
          onChange={(e) => setMessage(e.target.value)} // Update message as user types
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()} // Send on Enter key
        ></textarea>
        <button className="send-button" onClick={handleSend}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
