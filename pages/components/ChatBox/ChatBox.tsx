"use client"

import { useState } from "react";
import { Message } from "./Message/Message";

import styles from './ChatBox.module.css'
export function ChatBox() {
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState("");
  const [events, setEvents] = useState<any[]>([]);

  const handleKeyDown = async (e: any) => {
    if (e.key === "Enter" && input.trim() !== "") {
      setMessages([...messages, input]);
      const a = input
      setInput("");

      try {
        const response = await fetch("http://localhost:5000/api/python", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ prompt: a }),
        });

        if (response.ok) {
          const data: any[] = await response.json();

          data.forEach(event => {
            setEvents([...events, event])
          });
        } else {
          console.log("no res")
        }
      } 
      catch (error) {
        console.log(error)
      }
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