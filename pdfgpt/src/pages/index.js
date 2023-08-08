import React from "react";
import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import { usePathname } from "next/navigation";

// this page is the main navigation page based on user session

// TODO
// 1. based on supabase component establish about session
// 2. if session is authenticate then login
// 3. if session is not authenticated then log out
// 4. add a sign out button to the nav bar & an icon with your email
// 5. clean up the layout - think about how it is organised. can you make it better?

export default function Home({ updateSessionState, sessionStatusRedirect }) {
  const [session, setSession] = useState(null);

  useEffect(() => {
    updateSessionState(session, setSession);
  }, []);

  useEffect(() => {
    sessionStatusRedirect(session);
  }, [session]);

  return <div>Loading...</div>;
}
