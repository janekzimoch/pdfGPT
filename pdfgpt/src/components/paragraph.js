export default function Paragraph({ bookTitle, page, paragraph }) {
  return (
    <div className="m-3 rounded-xl bg-gray-300 px-8 py-2">
      <div className="flex flex-row items-center">
        <div className="mr-3 rounded-lg bg-[#6096B4] px-4 py-[0.5] text-lg font-semibold">
          {bookTitle}
        </div>
        <div className="text-md mr-3 rounded-lg bg-[#93BFCF] px-4 py-[0.5]">
          Page: {page}
        </div>
      </div>
      <p className="py-2 text-justify text-sm leading-snug">{paragraph}</p>
    </div>
  );
}
