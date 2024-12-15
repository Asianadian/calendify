import styles from './Calendar.module.css'
export function Calendar() {
  return (
  <div className={styles.calendar}>
    <iframe src="https://calendar.google.com/calendar/embed?src=danielchen.mc%40gmail.com&ctz=America%2FToronto" style={{ border: '0', width: '100%', height: '100%' }} frameBorder="0" scrolling="no" id="calendar"></iframe>
  </div>
  );
}