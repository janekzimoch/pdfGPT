import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/router";
import pdfgpt from "../../public/pdfgpt.png";
import Signout from "../components/navbar_components/signout";
import UserIcon from "../components/navbar_components/userIcon";
import { useContext } from "react";
import { UserContext } from "./contexts/userContext";

export default function Menu({ signOut }) {
  const route = useRouter();
  const { user, setUser } = useContext(UserContext);
  console.log(user);

  return (
    <div>
      <nav className="relative left-0 w-screen bg-white bg-opacity-0">
        <div className="mx-auto flex max-w-screen-xl flex-wrap items-center justify-between py-2">
          <span className="flex items-center">
            <Image src={pdfgpt} className="mx-3 h-12 w-12" alt="pdfGPT" />
            <span className="self-center whitespace-nowrap text-2xl font-semibold">
              pdfGPT
            </span>
          </span>
          {user == null ? (
            ""
          ) : (
            <div className="mr-5 flex flex-row">
              <UserIcon email={user.email} />
              <Signout signOut={signOut} />
            </div>
          )}
        </div>
      </nav>
    </div>
  );
}
