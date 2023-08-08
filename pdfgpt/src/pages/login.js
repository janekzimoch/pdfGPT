import { Auth } from "@supabase/auth-ui-react";
import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import { ThemeSupa } from "@supabase/auth-ui-shared";
import Image from "next/image";
import pdfgpt from "../../public/pdfgpt.png";
import styles from "~/styles/login.module.css"; // Import the CSS module

const brandColor = "#6096B4";
const brandAccentColor = "#93BFCF";

export default function Login({
  supabase,
  navbarHeight,
  updateSessionState,
  sessionStatusRedirect,
}) {
  const [session, setSession] = useState(null);

  useEffect(() => {
    updateSessionState(session, setSession);
  }, []);

  useEffect(() => {
    sessionStatusRedirect(session);
  }, [session]);

  const height = {
    minHeight: `calc(100vh - ${navbarHeight}px)`,
  };

  return (
    <div className="flex items-center justify-center " style={height}>
      <div className="min-w-[400px] rounded-2xl bg-gray-100 bg-opacity-50 px-20 py-10">
        <span className="mb-5 flex items-center">
          <Image src={pdfgpt} className="mr-3 h-5 w-5" alt="pdfGPT" />
          <p>Sign in to start using pdfGPT </p>
        </span>
        <Auth
          supabaseClient={supabase}
          redirectTo="http://localhost:3000/"
          providers={[]}
          appearance={{
            theme: ThemeSupa,
            extend: true,
            variables: {
              default: {
                colors: {
                  brand: brandColor,
                  brandAccent: brandAccentColor,
                },
              },
            },
            style: {
              button: {
                borderRadius: "10px",
              },
              container: {},
              anchor: {},
              divider: {},
              label: {},
              input: { backgroundColor: "white", borderRadius: "10px" },
              loader: {},
              message: {},
            },
          }}
        />
      </div>
    </div>
  );
}
