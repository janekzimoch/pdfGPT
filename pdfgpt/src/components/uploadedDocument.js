export default function UploadedDocument({ index, doc_name, remove_document }) {
  return (
    <div className="my-2 flex h-fit w-full items-center justify-between rounded-md bg-gray-200">
      <span className="ml-4 break-all">{doc_name}</span>
      <span className="m-4" onClick={() => remove_document(index)}>
        <svg
          class="h-2 w-2"
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
      </span>
    </div>
  );
}
