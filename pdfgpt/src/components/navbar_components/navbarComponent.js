import React from "react";

export default function NavbarComponent({ children }) {
  return (
    <div className="m-2 cursor-pointer rounded-xl bg-gray-100 px-4 py-1 hover:bg-gray-200">
      {children}
    </div>
  );
}
