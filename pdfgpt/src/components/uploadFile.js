import LoadingSpinner from "./loadingSpinner";

export default function UploadFile({
  selectedFiles,
  isFilePicked,
  changeHandler,
  isLoading,
}) {
  // const field_style = isFilePicked ? "justify-top" : "justify-center";
  const shadow = isLoading ? "bg-gray-100 opacity-70" : "";

  return (
    <div>
      <div className={`flex w-full items-center justify-center ${shadow}`}>
        <label
          htmlFor="dropzone-file"
          className={`dark:hover:bg-bray-800 justify-top scrollbarV flex h-60 w-full cursor-pointer flex-col items-center overflow-auto rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 pt-10 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:hover:border-gray-500 dark:hover:bg-gray-600`}
        >
          <div className="flex flex-col items-center justify-center pb-6 pt-5">
            <svg
              className="mb-4 h-8 w-8 text-gray-500 dark:text-gray-400"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 20 16"
            >
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
              />
            </svg>
            <div className="mb-2 overflow-auto text-sm text-gray-500 dark:text-gray-400">
              {isFilePicked ? (
                <ul>
                  {selectedFiles.map((selectedFile) => (
                    <li key={selectedFile.name}>
                      <div className="pb-3">
                        <p>Filename: {selectedFile.name}</p>
                        <p>Filetype: {selectedFile.type}</p>
                        <p>Size in bytes: {selectedFile.size}</p>
                        <p>
                          lastModifiedDate:{" "}
                          {selectedFile.lastModifiedDate.toLocaleDateString()}
                        </p>
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <div>
                  <span className="font-semibold">Click to upload</span>
                  <span> or drag and drop</span>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    Curently only PDF documents are supported.
                  </p>
                </div>
              )}
            </div>
          </div>
          <form encType="multipart/form-data">
            <input
              id="dropzone-file"
              type="file"
              className="hidden"
              multiple
              accept="application/pdf"
              onChange={changeHandler}
            />
          </form>
        </label>
      </div>
      {isLoading ? (
        <div className="absolute inset-0 flex items-center justify-center">
          <LoadingSpinner />
        </div>
      ) : (
        ""
      )}
    </div>
  );
}
