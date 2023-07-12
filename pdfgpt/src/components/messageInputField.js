// components/messageField.js
import React, { useEffect, useRef, useState } from "react";

export default function MessageInputField({ onMessageSent }) {
  const textareaRef = useRef(null);
  const [currentValue, setCurrentValue] = useState(""); // you can manage data with it

  useEffect(() => {
    textareaRef.current.style.height = "0px";
    const scrollHeight = textareaRef.current.scrollHeight;
    textareaRef.current.style.height = scrollHeight + "px";
  }, [currentValue]);

  const buttonClicked = () => {
    onMessageSent(currentValue);
    setCurrentValue("");
  };

  return (
    <>
      <div className="absolute bottom-10 w-[50%]">
        <div className="relative mx-12 flex">
          <span className="relative inset-y-0 flex w-full items-start rounded-xl bg-gray-200 text-gray-600 placeholder-gray-600">
            <textarea
              name="user_input_message"
              placeholder="Write your message!"
              ref={textareaRef}
              value={currentValue}
              onChange={(e) => {
                setCurrentValue(e.target.value);
              }}
              className="relative my-3 ml-8 w-full resize-none bg-transparent focus:placeholder-gray-400 focus:outline-none"
            />
            <div className="relative right-0 top-0 hidden sm:flex">
              <button
                type="button"
                onClick={buttonClicked}
                className="m-3 inline-flex resize-none justify-center rounded-xl bg-[#6096B4] px-4 py-3 text-white transition duration-500 ease-in-out hover:bg-[#93BFCF] focus:outline-none"
              >
                <span className="font-bold">Send</span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  className="ml-2 h-6 w-6 rotate-90 transform"
                >
                  <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path>
                </svg>
              </button>
            </div>
          </span>
        </div>
      </div>
    </>
  );
}
