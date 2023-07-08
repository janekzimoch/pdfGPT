// components/layout.js

import Menu from "./menu";

export default function Layout({ children }) {
  return (
    <>
      <main className="flex min-h-screen flex-col items-center bg-gradient-to-b from-[#fbf2ca] to-[rgb(133,188,247)]">
        {children}
      </main>
    </>
  );
}
