const express = require("express");
const exphbs = require("express-handlebars");
const mysql = require("./utils/dbcon.js");
const app = express();
const port = process.env.PORT || 3650;

const {
	getAllQuery,
	insertQuery,
	deleteQuery,
	updateQuery,
	dropTableQuery,
	makeTableQuery,
	getFromIdQuery,
} = require("./utils/queries");

const { formatDate, revertDate } = require("./utils/helpers");

app.engine("handlebars", exphbs());
app.set("view engine", "handlebars");

app.use(express.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.static("public"));

app.listen(port, (req, res) => {
	console.log(`Listening on port ${port}`);
});

// build and render mySQL table with populated workouts
app.get("/", function (req, res, next) {
	const context = {};
	const results = [];

	mysql.pool.query(getAllQuery, (err, rows, fields) => {
		if (err) {
			next(err);
			return;
		}
		for (let row of rows) {
			results.push({
				id: row.id,
				name: row.name,
				reps: row.reps,
				weight: row.weight,
				unit: row.unit,
				date: row.date,
			});
		}
		context.data = results;
		res.render("home", context);
	});
});

// insert workout into db
app.post("/", function (req, res, next) {
	const context = {};
	const { name, reps, weight, unit, date } = req.body;

	if (!name) {
		console.log("Missing a required field.");
		return;
	}

	mysql.pool.query(
		insertQuery,
		[name, reps, weight, unit, formatDate(date)],
		(err, result) => {
			if (err) {
				next(err);
				return;
			}
			context.results = result.insertId;
			res.send(JSON.stringify(context));
		}
	);
});

app.delete("/", function (req, res, next) {
	const context = {};
	mysql.pool.query(deleteQuery, [req.query.id], (err, result) => {
		if (err) {
			next(err);
			return;
		}
		context.results = "Deleted" + result.changedRows + " rows.";
		res.render("home", context);
	});
});

app.get("/update", (req, res, next) => {
	const context = {};
	mysql.pool.query(getFromIdQuery, [req.query.id], function (err, result) {
		if (err) {
			next(err);
			return;
		}
		if (!result[0]) {
			return next("this ID doesn't exist.")
		}
		const { name, reps, weight, unit, date } = result[0];

		context.data = {
			id: req.query.id,
			name: name,
			reps: reps,
			weight: weight,
			unit: unit,
			date: revertDate(date),
		};
		res.render("update", context);
	});
});

app.get("/submitUpdate", (req, res, next) => {
	const { name, reps, weight, date, id } = req.query;
	let { unit } = req.query;

	if (unit == "lb") {
		unit = 0;
	} else {
		unit = 1;
	}

	mysql.pool.query(
		updateQuery,
		[name, reps, weight, unit, formatDate(date), id],
		(err, result) => {
			if (err) {
				next(err);
				return;
			}
			res.redirect("/");
		}
	);
});

app.get("/reset-table", (req, res, next) => {
	const context = {};
	mysql.pool.query(dropTableQuery, function (err) {
		mysql.pool.query(makeTableQuery, function (err) {
			context.results = "Table reset";
			res.redirect("/");
		});
	});
});

app.all("*", (req, res, next) => {
	next("Page not found", 404);
});

app.use((err, req, res, next) => {
	res.render("layouts/error", { err });
});
