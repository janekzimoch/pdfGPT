export default async function handler(req, res) {
  if (req.method === "PUT") {
    const response = await fetch("http://127.0.0.1:5328/api/document", {
      method: "PUT",
      body: JSON.stringify(req.body),
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => response.json());
    res.status(200).json(response);
  } else {
    res.status(403).send("Invalid method type, only POST allowed");
  }
}
