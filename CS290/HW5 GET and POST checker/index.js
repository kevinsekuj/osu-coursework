const express = require("express");
const exphbs = require("express-handlebars");
const app = express();
const port = process.env.PORT || 3000;

app.engine("handlebars", exphbs());
app.set("view engine", "handlebars");

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.listen(port, (req, res) => {
	console.log(`Listening on port ${port}`);
});

app.get("/", (req, res) => {
	const queryParams = [];
	for (let param in req.query) {
		queryParams.push({ name: param, value: req.query[param] });
	}
	const data = {};
	data.dataList = queryParams;
	res.render("home", { data });
});

app.post("/", (req, res) => {
	const body = [];
	const query = [];
	for (let param in req.body) {
		body.push({ name: param, value: req.body[param] });
	}

	for (let qParam in req.query) {
		query.push({ name: qParam, value: req.query[qParam] });
	}

	const context = {};
	context.dataList = body;
	context.dataListQuery = query;
	res.render("homePost", { context });
});

app.all("*", (req, res, next) => {
	next("Page not found", 404);
});

app.use((err, req, res, next) => {
	res.render("layouts/error", { err });
});
