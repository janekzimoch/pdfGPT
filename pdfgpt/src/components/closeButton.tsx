import close_icon from "../../public/close_icon.png";
import Image from "next/image";

type VoidFunction = () => void;
interface PropTypes {
  handleClose: VoidFunction;
  disabled: boolean;
}

export default function CloseButton({
  handleClose,
  disabled = false,
}: PropTypes) {
  return (
    <>
      <button
        disabled={disabled}
        className="p-2 hover:opacity-50"
        onClick={handleClose}
      >
        <Image src={close_icon} alt="close_icon" />
      </button>
    </>
  );
}
