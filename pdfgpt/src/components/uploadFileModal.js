import React, { useState } from "react";
import UploadFile from "./uploadFile";

export default function UploadFileModal() {
  const [showModal, setShowModal] = React.useState(false);
  const [selectedFile, setSelectedFile] = useState();
  const [isFilePicked, setIsFilePicked] = useState(false);

  const changeHandler = (event) => {
    console.log(event.target.files[0]);
    setSelectedFile(event.target.files[0]);
    setIsFilePicked(true);
  };

  function handleSubmission() {
    const fileInput = document.getElementById("pdfInput");

    const formData = new FormData();
    formData.append("file", selectedFile);
    var contents = Array.from(formData.entries());
    console.log(contents);
    console.log("1");
    console.log(typeof selectedFile);
    console.log(typeof formData);
    // console.log(formData);
    // console.log(selectedFile);
    fetch("api/document", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        console.log("Success:", result);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    setShowModal(false);
  }

  return (
    <>
      <button
        className="rounded-xl bg-sky-500 px-4 py-2 font-bold text-white hover:bg-sky-400"
        type="button"
        onClick={() => setShowModal(true)}
      >
        Upload document
      </button>
      {showModal ? (
        <>
          <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto overflow-x-hidden outline-none focus:outline-none">
            <div className="relative mx-auto my-6 w-1/2 max-w-3xl">
              {/*content*/}
              <div className="relative flex w-full flex-col rounded-lg border-0 bg-white shadow-lg outline-none focus:outline-none">
                <div className="relative flex-auto p-6">
                  <UploadFile
                    selectedFile={selectedFile}
                    isFilePicked={isFilePicked}
                    changeHandler={changeHandler}
                  />
                </div>
                {/*footer*/}
                <div className="flex items-center justify-end rounded-b border-t border-solid border-slate-200 p-6">
                  <button
                    className="background-transparent mb-1 mr-1 px-6 py-2 text-sm font-bold uppercase text-red-500 outline-none transition-all duration-150 ease-linear focus:outline-none"
                    type="button"
                    onClick={() => setShowModal(false)}
                  >
                    Close
                  </button>
                  <button
                    className="mb-1 mr-1 rounded bg-emerald-500 px-6 py-3 text-sm font-bold uppercase text-white shadow outline-none transition-all duration-150 ease-linear hover:shadow-lg focus:outline-none active:bg-emerald-600"
                    type="button"
                    onClick={handleSubmission}
                  >
                    Upload
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div className="fixed inset-0 z-40 bg-black opacity-25"></div>
        </>
      ) : null}
    </>
  );
}
