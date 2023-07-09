export const config = {
  api: {
    bodyParser: false,
  },
};

import formidable from "formidable";
import { promises as fs } from "fs";

export default async function handler(req, res) {
  const form = formidable({}); //.IncomingForm();
  // const data = await new Promise((resolve, reject) => {
  //   const form = formidable({}); //.IncomingForm();
  //   form.parse(req, (err, fields, files) => {
  //     if (err) return reject(err);
  //     resolve({ fields, files });
  //   });
  // });
  // console.log(data.files.file[0].filepath);
  // // read file from the temporary path
  // const contents = await fs.readFile(data.files.file[0].filepath, {
  //   encoding: "utf8",
  // });
  // console.log(contents);

  form.parse(req, async (err, fields, files) => {
    console.log("files:", files.file);
    const formData = new FormData();
    formData.append("file", files.file[0]);
    console.log(files.file[0]);
    const response = await fetch("http://127.0.0.1:5328/api/document", {
      method: "POST",
      body: JSON.stringify({
        filepath: files.file[0].filepath,
        filename: files.file[0].originalFilename,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => response.json());
    res.status(200).json(response);
  });
}
