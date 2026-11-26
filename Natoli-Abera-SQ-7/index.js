const express = require("express");

const app = express();

// Middleware
app.use((req, res, next) => {
    console.log("Someone visited the website!");

    next();
});

// Route
app.get("/", (req, res) => {
    res.send("Welcome to my website!");
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});