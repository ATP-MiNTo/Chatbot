import React, { useState } from "react";
import './App.css';

function App() {
  const [messages, setMessages] = useState([{ text: "สวัสดี! ฉันคือ Flower Chat Bot 💬", sender: "bot" }]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (input.trim() === "") return;
    setMessages([...messages, { text: input, sender: "user" }]);
    setTimeout(() => {
      setMessages((prev) => [...prev, { text: "อยากรู้อะไรถามมาเลย!", sender: "bot" }]);
    }, 1000);
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
            <div key={index} className={`message ${msg.sender}`}>{msg.text}</div>
          ))}
        </div>
        <div className="chat-input">
          <input type="text" value={input} onChange={(e) => setInput(e.target.value)} placeholder="พิมพ์ข้อความ..." />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
