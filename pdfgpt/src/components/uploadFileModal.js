import React, { useState } from "react";
import UploadFile from "./uploadFile";
import CloseButton from "./closeButton";

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
      formData.append("files", file);
    });
    console.log(selectedFile);
    console.log(formData);
    console.log(formData.get("files"));
    // const file_names = selectedFile.map((x) => x.name);
    // await add_document(selectedFile, file_names);
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
        className="h-10 rounded-xl bg-[#6096B4] px-4 py-2 font-bold text-white hover:bg-[#93BFCF]"
        type="button"
        onClick={() => setShowModal(true)}
      >
        Upload document
      </button>
      {showModal ? (
        <>
          <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto overflow-x-hidden outline-none focus:outline-none">
            <div className="relative mx-auto my-6 w-1/2 max-w-3xl">
              <div className="relative flex w-full flex-col rounded-2xl border-0 bg-white shadow-lg outline-none focus:outline-none">
                <div className="relative flex-auto p-6 pb-4 pt-12">
                  <UploadFile
                    selectedFiles={selectedFile}
                    isFilePicked={isFilePicked}
                    changeHandler={changeHandler}
                    isLoading={isLoading}
                  />
                </div>
                <div className="absolute right-2 top-2 h-auto w-8">
                  <CloseButton disabled={isLoading} handleClose={handleClose} />
                </div>
                <div className="mb-4 mr-10 flex flex-row justify-end">
                  <button
                    className="h-10 rounded-xl bg-[#6096B4] px-4 py-2 font-bold text-white hover:bg-[#93BFCF]"
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
