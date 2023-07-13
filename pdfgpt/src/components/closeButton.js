import close_icon from "../../public/close_icon.png";
import Image from "next/image";

export default function CloseButton({ handleClose, disabled = false }) {
  return (
    <>
      <button
        disabled={disabled}
        className="p-2 hover:opacity-50"
        onClick={handleClose}
      >
        <Image src={close_icon} alt="close_icon" />

        {/* <svg
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
        </svg> */}
      </button>
    </>
  );
}
