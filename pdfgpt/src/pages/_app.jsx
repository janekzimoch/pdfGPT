import "~/styles/globals.css";
import "~/styles/spinner.css";
import Layout from "../components/layout";

const MyApp = ({ Component, pageProps: { session, ...pageProps } }) => {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
};

export default MyApp;
