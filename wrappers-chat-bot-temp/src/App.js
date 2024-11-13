import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello, how can I help you today?' } // Initial bot message
  ]);
  const [useWrapper, setUseWrapper] = useState(false);
  const [file, setFile] = useState(null);

  // Reference for the hidden file input
  const fileInputRef = useRef(null);

  // Handle file selection
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      // Process the selected file
      console.log("File selected:", selectedFile.name); // Optional: Logs the file name
      setFile(selectedFile);
      handleFileUpload(selectedFile); // Call your upload handler
    }
  };

  // Trigger file input click
  const handleChooseFileClick = () => {
    console.log("File input triggered"); // Optional: Check if this logs in the console
    fileInputRef.current.click(); // Programmatically click the hidden file input
  };

  // Validate filename
  const isValidFilename = (filename) => {
    return (
      filename.toLowerCase().startsWith('encs_degree_plan') &&
      filename.toLowerCase().endsWith('.xlsm')
    );
  };

  // Handle file upload
  const handleFileUpload = async (selectedFile) => {
    if (!selectedFile) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'bot', text: 'Please select a file to upload.' }
      ]);
      return;
    }

    // Check if filename is valid
    if (!isValidFilename(selectedFile.name)) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'bot', text: 'Error: Incorrect file uploaded. Please upload a valid ENCS Degree Plan file.' }
      ]);
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/upload/', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        // Display the confirmation message as a bot message
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', text: data.confirmation || 'File uploaded successfully!' }
        ]);

        // Display recommended classes if available
        if (data.recommended_classes && data.recommended_classes.length > 0) {
          const recommendedText = `Recommended classes: ${data.recommended_classes.join(', ')}`;
          setMessages((prevMessages) => [
            ...prevMessages,
            { sender: 'bot', text: recommendedText }
          ]);
        }
      } else {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', text: 'Error: Incorrect file uploaded.' }
        ]);
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'bot', text: 'Error: Could not upload file.' }
      ]);
    }
  };

  // Function to handle sending a message
  const handleSend = async () => {
    if (message.trim()) {
      setMessages([...messages, { sender: 'user', text: message }]);

      try {
        const response = await fetch("http://127.0.0.1:8000/chat/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ text: message, use_wrapper: useWrapper }),
        });

        const data = await response.json();
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', text: data.response },
        ]);
      } catch (error) {
        console.error("Error:", error);
      }

      setMessage('');
    }
  };

  return (
    <div className="App">
      <h1>ACM Education Chat Bot</h1>
      <img src="/acm-logo.png" alt="ACM Logo" className="header-image" />

      <div className="messages-container">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.sender === 'bot' ? 'bot-message' : 'user-message'}`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="chat-container">
        {/* Hidden file input for selecting files */}
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />

        {/* File upload button */}
        <button className="file-upload-button" onClick={handleChooseFileClick}>
          +
        </button>

        <textarea
          className="chat-input"
          placeholder="Type your message here..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
        ></textarea>

        <button className="send-button" onClick={handleSend}>Send</button>
      </div>

      <div className="model-selector">
        <label>
          <input
            type="checkbox"
            checked={useWrapper}
            onChange={() => setUseWrapper(!useWrapper)}
          />
          Use Wrapper Methods
        </label>
      </div>
    </div>
  );
}

export default App;
