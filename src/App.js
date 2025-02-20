import React, { useState } from "react";
import './App.css';

function App() {
  const [messages, setMessages] = useState([{ text: "สวัสดี! ฉันคือ Flower Chat Bot 💬", sender: "bot" }]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (input.trim() === "") return;

    // Add user message
    setMessages([...messages, { text: input, sender: "user", imageUrl: null }]);

    try {
      // Send user query to the Flask server
      const response = await fetch("http://127.0.0.1:5000/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: input }),
      });

      const data = await response.json();

      console.log(data);  // Log the entire response to inspect the structure

      const botResponse = data.response;
      const botImageUrl = data.image_url;

      // Add bot's response message
      setMessages((prev) => [
        ...prev,
        { text: botResponse, sender: "bot", imageUrl: botImageUrl },
      ]);

    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        { text: "Sorry, I couldn't fetch a response.", sender: "bot", imageUrl: null },
      ]);
    }

    setInput("");
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
            <div key={index} className={`message ${msg.sender}`}>
              <p>{msg.text}</p>
              {/* Render the image only if imageUrl exists */}
              {msg.imageUrl && <img src={msg.imageUrl} alt="Related content" className="bot-image" />}
            </div>
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
