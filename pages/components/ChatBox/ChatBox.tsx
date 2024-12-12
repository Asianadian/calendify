import styles from './ChatBox.module.css'
export function ChatBox() {
  return (
    <div className={styles.chatBox}>
      <h2>Chat</h2>
      <div className={styles.chatContent}>
        {/* Chat messages will go here */}
      </div>
      <input
        type="text"
        placeholder="Type a message..."
        className={styles.chatInput}
      />
    </div>
  );
}