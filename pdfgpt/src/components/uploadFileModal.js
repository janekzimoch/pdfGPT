import React, { useState } from "react";
import UploadFile from "./uploadFile";

export default function UploadFileModal({ add_document }) {
  const [showModal, setShowModal] = React.useState(false);
  const [selectedFile, setSelectedFile] = useState([]);
  const [isFilePicked, setIsFilePicked] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const changeHandler = (event) => {
    const files = event.target.files;
    const file_list = new Array(files.length);
    for (let i = 0; i < files.length; i++) {
      file_list[i] = files[i];
    }
    console.log(file_list);
    setSelectedFile(file_list);
    setIsFilePicked(true);
  };

  async function handleSubmission() {
    setIsLoading(true);
    if (selectedFile.length === 0) {
      return;
    }
    const formData = new FormData();
    const file_names = selectedFile.map((x) => x.name);
    selectedFile.forEach((file) => {
      formData.append("file", file);
    });

    await add_document(formData, file_names);
    setShowModal(false);
    setIsLoading(false);
    setIsFilePicked(false);
    setSelectedFile([]);
  }

  function handleClose() {
    setShowModal(false);
    setIsFilePicked(false);
    setSelectedFile([]);
  }

  return (
    <>
      <button
        className="h-10 rounded-xl bg-sky-500 px-4 py-2 font-bold text-white hover:bg-sky-400"
        type="button"
        onClick={() => setShowModal(true)}
      >
        Upload document
      </button>
      {showModal ? (
        <>
          <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto overflow-x-hidden outline-none focus:outline-none">
            <div className="relative mx-auto my-6 w-1/2 max-w-3xl">
              <div className="relative flex w-full flex-col rounded-lg border-0 bg-white shadow-lg outline-none focus:outline-none">
                <div className="relative flex-auto p-6">
                  <UploadFile
                    selectedFiles={selectedFile}
                    isFilePicked={isFilePicked}
                    changeHandler={changeHandler}
                    isLoading={isLoading}
                  />
                </div>
                <div className="flex items-center justify-end rounded-b border-t border-solid border-slate-200 p-6">
                  <button
                    className="background-transparent mb-1 mr-1 px-6 py-2 text-sm font-bold uppercase text-red-500 outline-none transition-all duration-150 ease-linear focus:outline-none"
                    type="button"
                    disabled={isLoading}
                    onClick={handleClose}
                  >
                    Close
                  </button>
                  <button
                    className="mb-1 mr-1 rounded bg-emerald-500 px-6 py-3 text-sm font-bold uppercase text-white shadow outline-none transition-all duration-150 ease-linear hover:shadow-lg focus:outline-none active:bg-emerald-600"
                    type="button"
                    disabled={isLoading}
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
