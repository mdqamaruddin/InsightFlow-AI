const express = require("express");
const app = express();

// 👇 ADD THIS PART HERE
app.get("/", (req, res) => {
  res.send("InsightFlow AI is live 🚀🔥");
});

// your other routes below
// app.get("/api/...", ...)

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});