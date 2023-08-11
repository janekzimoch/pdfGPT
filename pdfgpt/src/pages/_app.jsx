import "~/styles/globals.css";
import "~/styles/spinner.css";
import { useRouter } from "next/router";
import Layout from "../components/layout";
import { createClient } from "@supabase/supabase-js";
import { UserContext } from "../components/contexts/userContext";
import { useState, useEffect } from "react";

console.log(process.env.NEXT_PUBLIC_DB_SUPABASE_URL);

const MyApp = ({ Component, pageProps: { session, ...pageProps } }) => {
  const [user, setUser] = useState(null);
  const router = useRouter();

  useEffect(() => {
    updateUserState(getUser);
  }, []);

  console.log(process.env.NEXT_PUBLIC_DB_SUPABASE_URL);

  const supabase = createClient(
    process.env.NEXT_PUBLIC_DB_SUPABASE_URL,
    process.env.NEXT_PUBLIC_DB_SUPABASE_KEY
  );
  const navbarHeight = 50;

  async function updateUserState(getUser) {
    getUser().then((user_obj) => {
      setUser(user_obj.data.user);
    });
  }

  async function getUser() {
    const user = await supabase.auth.getUser();
    return user;
  }

  async function signOut() {
    const { error } = await supabase.auth.signOut();
    updateUserState(getUser);
    router.replace("/");
    return error;
  }

  function sessionStatusRedirect(session) {
    updateUserState(getUser);
    if (session) {
      router.replace("/app");
    } else {
      router.replace("/login");
    }
  }

  function updateSessionState(session, setSession) {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });
    return () => subscription.unsubscribe();
  }

  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Layout navbarHeight={navbarHeight} user={user} signOut={signOut}>
        <Component
          {...pageProps}
          supabase={supabase}
          updateSessionState={updateSessionState}
          sessionStatusRedirect={sessionStatusRedirect}
          navbarHeight={navbarHeight}
        />
      </Layout>
    </UserContext.Provider>
  );
};

export default MyApp;
