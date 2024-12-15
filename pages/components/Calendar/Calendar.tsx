import styles from './Calendar.module.css'
export function Calendar() {
  return (
  <div className={styles.calendar}>
    <iframe src="https://calendar.google.com/calendar/embed?src=4039edbbb48bad7cdbf3cc3ed8c746ba23edffb96f655ea948b6cd6f88a1e97b%40group.calendar.google.com&ctz=America%2FToronto" style={{ border: '0', width: '100%', height: '100%' }} frameBorder="0" scrolling="no" id="calendar"></iframe>
  </div>
  );
}