import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/router";
import pdfgpt from "../../public/pdfgpt.png";
import UploadFileModal from "./uploadFileModal";
import { useState } from "react";

export default function Menu({ setFaiss }) {
  const route = useRouter();

  return (
    <div>
      <nav className="relative left-0 w-screen bg-white bg-opacity-0">
        <div className="mx-auto flex max-w-screen-xl flex-wrap items-center justify-between p-1">
          <span className="flex items-center">
            <Image src={pdfgpt} className="mx-3 h-12 w-12" />
            <span className="self-center whitespace-nowrap text-2xl font-semibold">
              pdfGPT
            </span>
          </span>
          <div className="hidden w-full md:block md:w-auto" id="navbar-default">
            <ul className="mr-10 mt-4 flex flex-col">
              <li>
                <UploadFileModal setFaiss={setFaiss} />
                {/* <Link
                  href={"/"}
                  className="rounded-xl bg-sky-500 px-4 py-2 font-bold text-white hover:bg-sky-400"
                >
                  Upload document
                </Link> */}
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}
