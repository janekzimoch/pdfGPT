import Head from "next/head";
import Link from "next/link";
import MessageInputField from "../components/messageInputField";
import Message from "../components/message";
import { useState, useEffect, use } from "react";
import UploadFileModal from "../components/uploadFileModal";
import UploadedDocument from "../components/uploadedDocument";

const HOST_IP = "http://localhost:5328";
// "http://FastA-pdfgp-1ACE4VO8EB979-1556534170.eu-north-1.elb.amazonaws.com"; //"http://localhost:5328"; //http://0.0.0.0:5328"; //"http://127.0.0.1:5328"

export default function Home() {
  const [chat, setChat] = useState([]);
  const [documents, setDocuments] = useState([]);
  useEffect(() => {
    get_documents();
  }, []);

  // message functionality
  async function onMessageSent(text) {
    console.log(text);
    const usr_msg = {
      client: "user",
      message: text,
      paragraphs: [],
    };
    setChat((chat) => [...chat, usr_msg]);
    const chat_msg = await fetch(`${HOST_IP}/api/message`, {
      method: "POST",
      body: JSON.stringify(usr_msg),
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => response.json());
    console.log(chat_msg.paragraphs);
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

  // document functionality
  async function remove_document(index) {
    const filename = documents[index];
    console.log(filename);
    console.log(typeof filename);
    // remove document at 'index'
    var doc_array = documents.filter((doc, i) => i != index);
    setDocuments(doc_array);
    // update database
    const request_body = {
      filename: filename,
    };
    const result = await fetch(`${HOST_IP}/api/document`, {
      method: "PUT",
      body: JSON.stringify(request_body),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .catch((error) => console.error("Error:", error));
  }

  async function get_documents() {
    await fetch(`${HOST_IP}/api/document`)
      .then((response) => response.json())
      .then((result) => setDocuments(result["unique_titles"]))
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  async function add_document(formData, fileNames) {
    // send POST request to update FAISS
    console.log(formData);
    const result = await fetch(`${HOST_IP}/api/document`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .catch((error) => console.error("Error:", error));

    // add document to the document list
    setDocuments([...documents, ...fileNames]);
  }

  return (
    <div className="max-w-screen h-screen w-screen">
      <div className="grid h-[80%] w-screen grid-cols-4 gap-4">
        {/* this empty div below is needed to fill up left most column of 4 */}
        <div></div>
        <div className="col-span-2">
          <div className="relative h-[90%]">
            <div className="absolute inset-0 w-full items-center overflow-auto rounded-2xl bg-gray-100 bg-opacity-50 scrollbar">
              <div className="relative h-full max-h-[50%] min-h-[20%] w-full flex-col px-10 py-5">
                {chat.map((msg, i) => (
                  <Message
                    msg={msg}
                    key={i}
                    is_last_message={is_last_message(i)}
                  />
                ))}
              </div>
            </div>
          </div>
          <div className="relative mx-6 mb-8 mt-6 border-t-2 bg-gray-100 opacity-30"></div>
          <MessageInputField onMessageSent={onMessageSent} />
        </div>
        <div className="px-5">
          <div className="flex h-fit flex-col items-center justify-center rounded-2xl bg-gray-100 bg-opacity-70 p-3">
            <div className="">
              <UploadFileModal add_document={add_document} />
            </div>
            <ul className="w-full">
              {documents.map((doc_name, i) => (
                <li key={i}>
                  <UploadedDocument
                    index={i}
                    doc_name={doc_name}
                    remove_document={remove_document}
                  />
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
