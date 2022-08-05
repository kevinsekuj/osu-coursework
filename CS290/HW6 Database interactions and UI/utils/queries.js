module.exports.getAllQuery = "SELECT * from workout";

module.exports.insertQuery =
	"INSERT INTO workout (`name`, `reps`, `weight`, `unit`, `date`) VALUES (?, ?, ?, ?, ?)";

module.exports.deleteQuery = "DELETE FROM workout WHERE id=?";

module.exports.updateQuery =
	"UPDATE workout SET name=?, reps=?, weight=?, unit=?, date=? WHERE id=?";

module.exports.dropTableQuery = "DROP TABLE IF EXISTS workout";

module.exports.makeTableQuery = `CREATE TABLE workout( 
						id INT PRIMARY KEY AUTO_INCREMENT,
						name VARCHAR(255) NOT NULL,
						reps INT,
						weight INT,
						unit BOOLEAN,
						date VARCHAR(255))`;

module.exports.getFromIdQuery = "SELECT * FROM workout WHERE id=?";
