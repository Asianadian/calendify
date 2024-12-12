"use client"

import { useState } from "react";
import { Message } from "./Message/Message";

import styles from './ChatBox.module.css'
export function ChatBox() {
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState("");

  const handleKeyDown = (e: any) => {
    if (e.key === "Enter" && input.trim() !== "") {
      setMessages([...messages, input]);
      setInput("");
    }
  };

  return (
    <div className={styles.chatBox}>
      <div className={styles.chatContent}>
        {messages.map((msg, index) => (
          <Message key={index} text={msg} />
        ))}
      </div>
      <input
        type="text"
        placeholder="Type a message..."
        className={styles.chatInput}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
      />
    </div>
  );
}