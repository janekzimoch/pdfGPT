// components/layout.js
import Menu from "./menu";

export default function Layout({ children, navbarHeight, getUser, signOut }) {
  return (
    <div className={`{h-${navbarHeight}px}`}>
      <main className="max-w-screen max-h-screen min-h-screen flex-col items-center overflow-hidden bg-gradient-to-b from-[#EEE9DA] to-[#93BFCF]">
        <Menu getUser={getUser} signOut={signOut} />
        {children}
      </main>
    </div>
  );
}
