import { useState, useEffect } from "react";
import UseWebSocket from "../UseWebSocket";

function VoteConsumer({ roomName }) {
  const [votes, setVotes] = useState([]);

  const handleVoteUpdate = (data) => {
    if (data.action === "vote") {
      setVotes((prevVotes) => [...prevVotes, data.vote]);
    }
  };

  const sendVote = UseWebSocket(roomName, "vote", handleVoteUpdate);

  const handleSendVote = (vote) => {
    sendVote({ vote });
  };

  return (
    <div>
      <h2>Votes</h2>
      {votes.map((vote, idx) => (
        <div key={idx}>{vote}</div>
      ))}
      <button onClick={() => handleSendVote("Upvote")}>Upvote</button>
      <button onClick={() => handleSendVote("Downvote")}>Downvote</button>
    </div>
  );
}

export default VoteConsumer;
