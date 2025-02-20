import React, { useState } from "react";
import './App.css';
import axios from "axios"; // Import axios

function App() {
  const [messages, setMessages] = useState([{ text: "สวัสดี! ฉันคือ Flower Chat Bot 💬", sender: "bot" }]);
  const [input, setInput] = useState("");

  // Function to send user message to Flask backend and get response
  const sendMessage = async () => {
    if (input.trim() === "") return;

    // Add user's message to the chat
    setMessages([...messages, { text: input, sender: "user" }]);

    try {
      // Send request to Flask backend
      const response = await axios.post("http://127.0.0.1:5000/api/query", {
        query: input,
      });

      // Add the bot's response to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: response.data.response, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Error sending message to backend:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: "ขออภัย, เกิดข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์.", sender: "bot" },
      ]);
    }

    setInput(""); // Clear the input field
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="Topic">
          <b>F🌷ower 'CHAT' Space</b>
        </div>
        <p className="subtext">🌼 แชทบอทที่จะช่วยตอบทุกคำถามเกี่ยวกับดอกไม้ 🌼</p>
      </header>
      <div className="chat-container">
        <div className="chat-box">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>{msg.text}</div>
          ))}
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="พิมพ์ข้อความ..."
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
