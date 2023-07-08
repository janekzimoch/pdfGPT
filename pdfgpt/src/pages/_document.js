import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        {/* <title>chatGPT with your PDF</title> */}
        <meta name="description" content="chatGPT with your PDF" />
        <link rel="icon" href="/pdfgpt.png" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
