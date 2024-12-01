import { useState, useEffect } from "react";
import UseWebSocket from "../UseWebSocket";

function MemeConsumer({ roomName }) {
  const [meme, setMeme] = useState(null);

  const handleMemeUpdate = (data) => {
    if (data.action === "update_meme") {
      setMeme(data.meme_update);
    }
  };

  const sendMemeUpdate = UseWebSocket(roomName, "meme", handleMemeUpdate);

  const handleSendMemeUpdate = (memeUpdate) => {
    sendMemeUpdate({ meme_update: memeUpdate });
  };

  return (
    <div>
      <h2>Meme Update: {meme}</h2>
      <button onClick={() => handleSendMemeUpdate("New Meme")}>Update Meme</button>
    </div>
  );
}

export default MemeConsumer;
