"use client"

import { useState } from "react";
import { Message } from "./Message/Message";
import { Header } from "./Header/Header";

import styles from './ChatBox.module.css'
export function ChatBox() {
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState("");
  const [events, setEvents] = useState<any[]>([]);

  const refreshCalendar = () => {
    const d: any = document
    d.getElementById("calendar").src = d.getElementById("calendar").src;
  }

  const handleKeyDown = async (e: any) => {
    if (e.key === "Enter" && input.trim() !== "") {
      setMessages([...messages, input]);
      const prompt = input;
      setInput("");

      try {
        const response = await fetch("http://localhost:5000/api/langchain", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ prompt: prompt, events: events}),
        });

        if (response.ok) {
          const data: any[] = await response.json();
          console.log(data)
          data.forEach(event => {
            setEvents([...events, event])
          });

          refreshCalendar();
        } else {
          console.log("No response")
        }
      } 
      catch (error) {
        console.log(error)
      }
    }
  };

  return (
    <div className={styles.chatBox}>
      <Header />
      <div className={styles.chatContent}>
        {messages.map((msg, index) => (
          <Message key={index} text={msg} />
        ))}
      </div>
      <input
        type="text"
        placeholder="Message Calendify"
        className={styles.chatInput}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
      />
    </div>
  );
}