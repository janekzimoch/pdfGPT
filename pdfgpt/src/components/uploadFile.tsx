import LoadingSpinner from "./loadingSpinner";

type VoidFunction = () => void;
interface MyFile extends File {
  lastModifiedDate: any;
}

interface PropTypes {
  selectedFiles: MyFile[];
  isFilePicked: boolean;
  changeHandler: VoidFunction;
  isLoading: boolean;
}

export default function UploadFile({
  selectedFiles,
  isFilePicked,
  changeHandler,
  isLoading,
}: PropTypes) {
  // const field_style = isFilePicked ? "justify-top" : "justify-center";
  const shadow = isLoading ? "bg-gray-100 opacity-70" : "";

  return (
    <div>
      <div className={`flex w-full items-center justify-center ${shadow}`}>
        <label
          htmlFor="dropzone-file"
          className={`dark:hover:bg-bray-800 justify-top flex h-60 w-full cursor-pointer flex-col items-center overflow-auto rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 pt-10 scrollbar hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:hover:border-gray-500 dark:hover:bg-gray-600`}
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
                        <p>File name: {selectedFile.name}</p>
                        <p>File size: {niceBytes(selectedFile.size)}</p>
                        {/* <p>
                          Last modified:{" "}
                          {selectedFile.lastModifiedDate.toLocaleDateString()}
                        </p> */}
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <div>
                  <span className="font-semibold">Click to upload</span>
                  {/* <span> or drag and drop</span> */}
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

const units = ["bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"];

function niceBytes(x: number) {
  const x_str = String(x);
  let l: number = 0;
  let n: number = parseInt(x_str, 10) || 0;

  while (n >= 1024 && ++l) {
    n = n / 1024;
  }

  return n.toFixed(n < 10 && l > 0 ? 1 : 0) + " " + units[l];
}
