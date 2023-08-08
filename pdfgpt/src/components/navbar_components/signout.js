import React from "react";
import NavbarComponent from "./navbarComponent";

export default function Signout({ signOut }) {
  return (
    <NavbarComponent>
      <button onClick={signOut}>
        <p>Sign out</p>
      </button>
    </NavbarComponent>
  );
}
