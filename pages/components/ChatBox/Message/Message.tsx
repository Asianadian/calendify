type Props = {
  text: string
}

import styles from './Message.module.css'
export function Message(props: Props) {
  return <div className={styles.message}>{props.text}</div>;
}