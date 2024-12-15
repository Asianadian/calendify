import { ChatBox } from "../pages/components/ChatBox/ChatBox";
import { Calendar } from "../pages/components/Calendar/Calendar";

export default function Home() {
  return (
    <div className="container">
      <div className="content">
        <ChatBox />
        <Calendar />
      </div>
    </div>
  );
}
