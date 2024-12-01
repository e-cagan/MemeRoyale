import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BASE_URL } from '../constants';

function RoomDetailModal({ roomId, isOpen, closeModal }) {
  const [roomDetails, setRoomDetails] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (roomId && isOpen) {
      const fetchRoomDetails = async () => {
        try {
          const response = await axios.get(`${BASE_URL}/rooms/${roomId}`);
          setRoomDetails(response.data);
        } catch (err) {
          setError('Oda detayları yüklenirken bir hata oluştu.');
        }
      };

      fetchRoomDetails();
    }
  }, [roomId, isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-75 z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-1/2">
        <h2 className="text-2xl font-semibold mb-4">Oda Detayları</h2>
        {error ? (
          <p className="text-red-500">{error}</p>
        ) : (
          roomDetails && (
            <div>
              <p><strong>Oda Adı:</strong> {roomDetails.name}</p>
              <p><strong>Oda Sahibi:</strong> {roomDetails.host.username}</p>
              <p><strong>Katılımcılar:</strong> {roomDetails.participants.map(p => p.username).join(', ')}</p>
              <p><strong>Durum:</strong> {roomDetails.status}</p>
            </div>
          )
        )}
        <div className="flex justify-end mt-4">
          <button onClick={closeModal} className="bg-blue-500 text-white py-2 px-4 rounded-lg">Kapat</button>
        </div>
      </div>
    </div>
  );
}

export default RoomDetailModal;
