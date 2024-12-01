import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import CreateRoomModal from './CreateRoomModal';
import RoomDetailModal from './RoomDetailModal'; // Yeni import
import { BASE_URL } from '../constants';

function HomePage() {
  const [latestRooms, setLatestRooms] = useState([]);
  const [latestUsers, setLatestUsers] = useState([]);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedRoomId, setSelectedRoomId] = useState(null); // Seçilen oda ID'si
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHomePageData = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/`);
        setLatestRooms(response.data.latest_rooms);
        setLatestUsers(response.data.latest_users);
        setIsLoading(false);
      } catch (err) {
        setError("Ana sayfa verileri yüklenirken bir hata oluştu.");
        setIsLoading(false);
      }
    };

    fetchHomePageData();
  }, []);

  const handleJoinRoom = (roomId) => {
    navigate(`/rooms/join/${roomId}`);
  };

  const openModal = (roomId) => {
    setSelectedRoomId(roomId);
  };

  const closeModal = () => {
    setSelectedRoomId(null);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Veriler yükleniyor...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center py-10">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-2xl">
        <h1 className="text-4xl font-bold text-center text-blue-500 mb-6">MemeRoyale</h1>
        <p className="text-center text-gray-600 mb-6">Oda oluşturun, katılın ve oyunu başlatın!</p>

        <div className="mb-6 text-center">
          <button
            onClick={() => setIsModalOpen(true)}
            className="py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600"
          >
            Oda Oluştur
          </button>
        </div>

        <div className="mb-6">
          <h2 className="text-2xl font-semibold mb-4">Son Oluşturulan Odalar</h2>
          {error ? (
            <p className="text-red-500">{error}</p>
          ) : (
            <ul className="space-y-4">
              {latestRooms && latestRooms.length > 0 ? (
                latestRooms.map((room) => (
                  <li key={room.id} className="flex justify-between items-center p-4 bg-gray-200 rounded-lg shadow-md">
                    <span className="text-lg font-medium">{room.name}</span>
                    <button
                      onClick={() => handleJoinRoom(room.id)}
                      className="py-2 px-4 bg-green-500 text-white rounded-lg"
                    >
                      Odaya Katıl
                    </button>
                    <button
                      onClick={() => openModal(room.id)} // Modal açma
                      className="py-2 px-4 bg-blue-500 text-white rounded-lg ml-2"
                    >
                      Detaylar
                    </button>
                  </li>
                ))
              ) : (
                <p>Henüz oluşturulmuş oda yok.</p>
              )}
            </ul>
          )}
        </div>

        <div>
          <h3 className="text-2xl font-semibold mb-4">Son Katılan Kullanıcılar</h3>
          <ul className="space-y-2">
            {latestUsers && latestUsers.length > 0 ? (
              latestUsers.map((user) => (
                <li key={user.id} className="text-lg text-gray-700">{user.username}</li>
              ))
            ) : (
              <p>Henüz katılan kullanıcı yok.</p>
            )}
          </ul>
        </div>
      </div>

      {/* Oda Detayları Modalı */}
      <RoomDetailModal roomId={selectedRoomId} isOpen={selectedRoomId !== null} closeModal={closeModal} />
      
      {/* Oda Oluşturma Modalı */}
      <CreateRoomModal
        isOpen={isModalOpen}
        closeModal={() => setIsModalOpen(false)}
      />
    </div>
  );
}

export default HomePage;
