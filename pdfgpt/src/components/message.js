// components/message.js
import Image from "next/image";
import pdfgpt from "../../public/pdfgpt.png";
import user_icon from "../../public/user_icon.png";
import { useState } from "react";
import MessageModal from "./messageModal";

export default function Message(props) {
  const [showModal, setShowModal] = useState(false);
  const is_chat = props.msg.client === "chat";
  const justify_style = is_chat ? "justify-start" : "justify-end";
  const rounded_none = is_chat ? "bl" : "br";
  const order_msg = is_chat ? "order-2" : "order-1";
  const order_icon = is_chat ? "order-1" : "order-2";

  function closeModal() {
    setShowModal(false);
  }

  return (
    <>
      <div
        className={`chat-message ${props.is_last_message ? "pb-3" : "pb-1"}`}
      >
        <div className={`flex items-end ${justify_style}`}>
          <div
            className={`${order_msg} mx-2 flex max-w-xs flex-col space-y-2 text-xs`}
          >
            {is_chat ? (
              <div onClick={() => setShowModal(true)}>
                <span
                  className={`inline-block rounded-lg ${
                    props.is_last_message ? `rounded-${rounded_none}-none` : ""
                  } bg-[#BDCDD6] px-4 py-2 text-gray-600 hover:bg-[#93BFCF]`}
                >
                  <p className="break-words">{props.msg.message}</p>
                </span>
              </div>
            ) : (
              <div>
                <span
                  className={`inline-block rounded-lg ${
                    props.is_last_message ? `rounded-${rounded_none}-none` : ""
                  } bg-gray-300 px-4 py-2 text-gray-600`}
                >
                  <p className="break-all">{props.msg.message}</p>
                </span>
              </div>
            )}
          </div>
          {props.is_last_message ? (
            <Image
              alt={""}
              src={is_chat ? pdfgpt : user_icon}
              className={`${order_icon}  h-6 w-6`}
            />
          ) : (
            <Image
              alt={""}
              src={pdfgpt}
              className={`${order_icon}  h-6 w-6 opacity-0`}
            />
          )}
        </div>
      </div>
      {showModal ? (
        <MessageModal
          paragraphs={props.msg.paragraphs}
          closeModal={closeModal}
        />
      ) : null}
    </>
  );
}
