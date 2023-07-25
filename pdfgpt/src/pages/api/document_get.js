export default async function handler(req, res) {
  if (req.method === "GET") {
    const response = await fetch("http://127.0.0.1:5328/api/document", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => response.json());
    res.status(200).json(response);
  } else {
    res
      .status(403)
      .send(
        "Invalid method type, only GET allowed, try document_remove or documnet_upload."
      );
  }
}
