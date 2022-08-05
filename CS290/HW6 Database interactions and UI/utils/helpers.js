module.exports.formatDate = date =>
	date.toString().substring(5, date.length) +
	"-" +
	date.toString().slice(0, 4);

module.exports.revertDate = date => date.slice(-4) + "-" + date.slice(0, 5);
