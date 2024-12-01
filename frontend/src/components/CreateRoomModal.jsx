import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BASE_URL, ACCESS_TOKEN } from "../constants";

function CreateRoomModal({ isOpen, closeModal, handleRoomCreated }) {
  const [roomName, setRoomName] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isOpen) {
      setRoomName(''); // Modal kapatıldığında input sıfırlanır
      setError(null);  // Hatalar temizlenir
    }
  }, [isOpen]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isLoading) return; // Çift isteği engelle
    if (!roomName.trim()) {
      setError("Oda adı boş olamaz!");
      return;
    }

    setIsLoading(true);
    setError(null);

    const token = localStorage.getItem(`${ACCESS_TOKEN}`);
    console.log(token)

    if (!token) {
      setError("Giriş yapmanız gerekiyor.");
      setIsLoading(false);
      return;
    }

    try {
      const response = await axios.post(
        `${BASE_URL}/rooms/create`,
        { name: roomName },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      handleRoomCreated(response.data); // Yeni oda verisini parent'e aktar
      closeModal(); // Modalı kapat
    } catch (err) {
      if (err.response) {
        setError(err.response.data.detail || "Oda oluşturulurken bir hata oluştu.");
      } else {
        setError("Sunucuyla bağlantı kurulamadı.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      className={`fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center transition-opacity ${isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
    >
      <div className="bg-white rounded-lg w-96 p-6 shadow-lg">
        <h2 className="text-2xl font-semibold text-center mb-4">Create Room</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="roomName" className="block text-sm font-medium text-gray-700">Room Name</label>
            <input
              id="roomName"
              type="text"
              value={roomName}
              onChange={(e) => setRoomName(e.target.value)}
              placeholder="Enter Room Name"
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <div className="flex justify-between">
            <button
              onClick={closeModal}
              className="px-4 py-2 bg-gray-300 rounded-lg text-gray-700 hover:bg-gray-400"
            >
              Close
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300"
              disabled={isLoading}
            >
              {isLoading ? "Creating Room..." : "Create Room"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateRoomModal;
