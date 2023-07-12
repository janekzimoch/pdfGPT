// components/layout.js

import Menu from "./menu";

export default function Layout({ children }) {
  return (
    <>
      <main className="max-w-screen max-h-screen min-h-screen flex-col items-center overflow-hidden bg-gradient-to-b from-[#EEE9DA] to-[#93BFCF]">
        <Menu />
        {children}
      </main>
    </>
  );
}
