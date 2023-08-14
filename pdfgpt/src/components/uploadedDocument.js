import CloseButton from "./closeButton";

export default function UploadedDocument({ index, doc_name, remove_document }) {
  return (
    <div className="relative my-2 flex h-fit w-full items-center rounded-md bg-gray-200  shadow-md">
      <span className="ml-4 mr-10 break-all">{doc_name}</span>
      <span className="absolute right-1 h-auto w-7">
        <CloseButton handleClose={() => remove_document(index)} />
      </span>

      {/* <span className="m-4" onClick={() => remove_document(index)}>
        <svg
          className="h-2 w-2"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 14 14"
        >
          <path
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
          />
        </svg>
      </span> */}
    </div>
  );
}
