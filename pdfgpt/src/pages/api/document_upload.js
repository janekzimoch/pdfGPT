export const config = {
  api: {
    bodyParser: false,
  },
};

import formidable from "formidable";
import { promises as fs } from "fs";

export default async function handler(req, res) {
  if (req.method === "POST") {
    const form = formidable({});
    form.parse(req, async (err, fields, files) => {
      const formData = new FormData();
      formData.append("file", files.file[0]);
      const response = await fetch("http://127.0.0.1:5328/api/document", {
        method: "POST",
        body: JSON.stringify({
          filepath: files.file.map((f) => f.filepath),
          filename: files.file.map((f) => f.originalFilename),
        }),
        headers: {
          "Content-Type": "application/json",
        },
      }).then((response) => response.json());

      res.status(200).json(response);
    });
  } else {
    res.status(403).send("Invalid method type, only POST allowed");
  }
}
