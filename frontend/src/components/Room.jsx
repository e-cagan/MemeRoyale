import React, { useState } from "react";
import axios from "axios";
import { BASE_URL } from "../constants";
import { useNavigate } from "react-router-dom";
import UseWebSocket from "../useWebSocket"; // WebSocket hook

function Room() {
  const [roomName, setRoomName] = useState("");
  const [roomId, setRoomId] = useState("");
  const [isHost, setIsHost] = useState(false);
  const [gameStarted, setGameStarted] = useState(false);
  const [participants, setParticipants] = useState([]);
  const [timeLeft, setTimeLeft] = useState(null);
  const navigate = useNavigate();

  const handleRoomCreate = async () => {
    if (roomName) {
      try {
        // Oda oluşturma işlemi
        const response = await axios.post(`${BASE_URL}/rooms/create`, { roomName });
        
        if (response.status === 200) {
          setIsHost(true); // Odayı oluşturan kişi host olur
          alert("Oda başarıyla oluşturuldu!");
        }
      } catch (error) {
        console.error("Oda oluşturulurken hata oluştu:", error);
        alert("Oda oluşturulamadı.");
      }
    }
  };

  const handleJoinRoom = async () => {
    if (roomId) {
      try {
        // ID ile katılma isteği
        const response = await axios.get(`${BASE_URL}/rooms/join/${roomId}`);
        
        if (response.status === 200) {
          // Başarıyla katıldı, odaya yönlendir
          navigate(`${BASE_URL}/room/${roomId}`);
        }
      } catch (error) {
        console.error("Odaya katılma hatası:", error);
        alert("Odaya katılma sırasında bir hata oluştu.");
      }
    }
  };

  const handleStartGame = () => {
    if (isHost) {
      setGameStarted(true);
      // WebSocket üzerinden oyunu başlatma komutu gönderilebilir
    }
  };

  const handleTimerUpdate = (data) => {
    if (data.action === "timer") {
      setTimeLeft(data.time_left);
    }
  };

  const sendGameStart = UseWebSocket(roomName, "timer", handleTimerUpdate);

  return (
    <div>
      <h2>MemeRoyale</h2>
      <input
        type="text"
        placeholder="Oda Adı"
        value={roomName}
        onChange={(e) => setRoomName(e.target.value)}
      />
      <button onClick={handleRoomCreate}>Oda Oluştur</button>
      <button onClick={handleJoinRoom}>Odaya Katıl</button>

      {isHost && !gameStarted && (
        <button onClick={handleStartGame}>Oyunu Başlat</button>
      )}

      {gameStarted && (
        <div>
          <h3>Game Started!</h3>
          <p>Zaman: {timeLeft} saniye kaldı</p>
        </div>
      )}

      <div>
        <h3>Participants:</h3>
        {participants.map((participant, idx) => (
          <div key={idx}>{participant.username}</div>
        ))}
      </div>
    </div>
  );
}

export default Room;
