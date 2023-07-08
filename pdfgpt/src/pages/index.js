import Head from "next/head";
import Link from "next/link";
import MessageInputField from "../components/messageInputField";
import Message from "../components/message";
import { useState, useEffect } from "react";

// {
//   client: "user",
//   time: 1,
//   message: "hello",
// },
// {
//   client: "chat",
//   time: 2,
//   message: "hello",
// },
// {
//   client: "user",
//   time: 3,
//   message: "tell me...",
// },
// {
//   client: "user",
//   time: 5,
//   message: "how are you?",
// },
// {
//   client: "chat",
//   time: 6,
//   message: "im fine thanks",
// },
// {
//   client: "chat",
//   time: 7,
//   message:
//     "A path from a point approximately 330 metres east of the most south westerly corner of 17 Batherton Close, Widnes and approximately 208 metres east-south-east of the most southerly corner of Unit 3 Foundry Industrial Estate, Victoria Street, Widnes, proceeding in a generally east-north-easterly direction for approximately 28 metres to a point approximately 202 metres east-south-east of the most south-easterly corner of Unit 4 Foundry Industrial Estate, Victoria Street, and approximately 347 metres east of the most south-easterly corner of 17 Batherton Close, then proceeding in a generally northerly direction ",
// },
// {
//   client: "chat",
//   time: 8,
//   message:
//     "for approximately 21 metres to a point approximately 210 metres east of the most south-easterly corner of Unit 5 Foundry Industrial Estate,",
// },

const messages_json = [];

export default function Home() {
  const [chat, setChat] = useState(messages_json);

  async function onMessageSent(text) {
    console.log(text);
    const usr_msg = {
      client: "user",
      time: 1000, // TBD
      message: text,
    };
    setChat((chat) => [...chat, usr_msg]);
    const chat_msg = await fetch("/api/message", {
      method: "POST",
      body: JSON.stringify(usr_msg),
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => response.json());
    setChat((chat) => [...chat, chat_msg]);
  }

  function is_last_message(i) {
    const current_msg = chat[i];
    if (i + 1 < chat.length) {
      const next_msg = chat[i + 1];
      if (current_msg.client === next_msg.client) {
        return false;
      }
    }
    return true;
  }

  return (
    <>
      <div className="flex w-screen flex-col items-center">
        <div className="m-10 flex min-h-full w-7/12 flex-col rounded-2xl bg-gray-100 bg-opacity-70 p-10">
          {chat.map((msg, i) => (
            <Message
              msg={msg}
              key={msg.time}
              is_last_message={is_last_message(i)}
            />
          ))}
        </div>
        <MessageInputField onMessageSent={onMessageSent} />
      </div>
    </>
  );
}

// async function get_api_response() {
//   fetch("http://127.0.0.1:5328/api/document", {
//     method: "GET",
//     mode: 'no-cors',
//     headers: {
//       'Content-Type': "application/json",
//     },
//   }
//   ).then((response) => response.json()).then((res) => console.log(res));
// }
