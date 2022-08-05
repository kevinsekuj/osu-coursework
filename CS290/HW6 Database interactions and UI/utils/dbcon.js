const mysql = require("mysql");

const pool = mysql.createPool({
	connectionLimit: 10,
	host: "classmysql.engr.oregonstate.edu",
	user: "cs290_sekujk",
	password: "3648",
	database: "cs290_sekujk",
});

module.exports.pool = pool;
