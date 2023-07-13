import React, { useState } from "react";
import Paragraph from "./paragraph";
import CloseButton from "./closeButton";

const paragraphs = [
  {
    bookTitle: "title1",
    page: "45",
    paragraph:
      "simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.",
  },
  {
    bookTitle: "title1",
    page: "45",
    paragraph:
      "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using",
  },
];

export default function MessageModal({ paragraphs, closeModal }) {
  return (
    <>
      <div className="fixed inset-0 z-50 flex items-center justify-center outline-none focus:outline-none">
        <div className="relative h-4/5 w-4/5 justify-center rounded-2xl bg-gray-100">
          <div className="m-10 flex h-4/5 flex-col overflow-auto scrollbar">
            {paragraphs.map((pr, i) => (
              <Paragraph
                key={i}
                bookTitle="TBD" //{pr.bookTitle}
                page="100" //{pr.page}
                paragraph={pr.paragraph}
              />
            ))}
          </div>
          <div className="absolute right-2 top-2 h-auto w-8">
            <CloseButton handleClose={closeModal} />
          </div>
        </div>
      </div>
      <div className="fixed inset-0 z-40 bg-black opacity-25"></div>
    </>
  );
}
