export default async function handler(req, res) {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Headers", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");

    if (req.method === "OPTIONS") {
        return res.status(200).end();
    }

    const url = req.query.url;

    if (!url) {
        return res.status(400).send("Missing url");
    }

    if (!url.startsWith("http://") && !url.startsWith("https://")) {
        return res.status(400).send("Invalid url");
    }

    try {
        const response = await fetch(url);
        const contentType = response.headers.get("content-type") || "text/plain";
        const body = await response.text();

        res.setHeader("Content-Type", contentType);
        res.status(200).send(body);
    } catch (err) {
        res.status(500).send("Error fetching: " + err.message);
    }
          }
