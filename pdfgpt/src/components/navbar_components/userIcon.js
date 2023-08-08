import React from "react";
import NavbarComponent from "./navbarComponent";

export default function UserIcon({ email }) {
  return (
    <NavbarComponent>
      <p>{email}</p>
    </NavbarComponent>
  );
}
