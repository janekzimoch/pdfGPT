import React, { useState } from "react";
import Paragraph from "./paragraph";
import CloseButton from "./closeButton";

export default function MessageModal({ paragraphs, closeModal }) {
  return (
    <>
      <div className="fixed inset-0 z-50 flex items-center justify-center outline-none focus:outline-none">
        <div className="fixed h-4/5 w-4/5 items-center justify-center rounded-2xl bg-gray-100 shadow-md ">
          <div className="h-full p-10">
            <div className="flex h-full flex-col overflow-auto scrollbar">
              {paragraphs.map((pr, i) => (
                <Paragraph
                  key={i}
                  bookTitle={pr.title}
                  page={pr.page}
                  paragraph={pr.paragraph}
                />
              ))}
            </div>
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
