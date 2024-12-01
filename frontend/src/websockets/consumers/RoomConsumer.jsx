import { useState, useEffect } from "react";
import UseWebSocket from "../UseWebSocket";

function RoomConsumer({ roomName }) {
  const [messages, setMessages] = useState([]);

  const handleMessageReceived = (data) => {
    if (data.type === "chat_message") {
      setMessages((prevMessages) => [
        ...prevMessages,
        { username: data.username, message: data.message, timestamp: data.timestamp },
      ]);
    }
  };

  const sendMessage = UseWebSocket(roomName, "chat", handleMessageReceived);

  const handleSendMessage = (message) => {
    sendMessage({ message });
  };

  return (
    <div>
      <h2>Chat Messages</h2>
      {messages.map((msg, idx) => (
        <div key={idx}>
          <strong>{msg.username}</strong>: {msg.message} <em>{msg.timestamp}</em>
        </div>
      ))}
      <input type="text" onChange={(e) => handleSendMessage(e.target.value)} placeholder="Type a message" />
    </div>
  );
}

export default RoomConsumer;
