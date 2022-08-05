const tbody = document.querySelector("tbody");

document.getElementById("postSubmit").addEventListener("click", function (e) {
	const req = new XMLHttpRequest();
	const data = {
		workout: null,
		reps: null,
		weight: null,
		unit: null,
		date: null,
	};
	const values = [];
	let unit;

	data.name = document.getElementById("workout").value;
	data.reps = document.getElementById("reps").value;
	data.weight = document.getElementById("weight").value;
	data.date = document.getElementById("date").value;

	if (document.getElementById("pound").checked) {
		data.unit = 0;
		unit = "lb";
	} else {
		data.unit = 1;
		unit = "kg";
	}

	let dateVal = document.getElementById("date").value;
	const date =
		dateVal.substring(5, dateVal.length) + "-" + dateVal.slice(0, 4);

	values.push(data.name, data.reps, data.weight, unit, date);

	req.open("POST", "/", true);
	req.setRequestHeader("Content-Type", "application/json");

	// values array contains request parameters. iterate with forEach creating
	// new row at end of table and insert cells with index corresponding to value

	req.addEventListener("load", function () {
		let res = JSON.parse(req.responseText);
		let updateBtn = document.createElement("button");
		let deleteBtn = document.createElement("button");

		updateBtn.textContent = "Edit";
		deleteBtn.textContent = "Delete";

		// append ID and inputs for edit/delete
		values.push(updateBtn, deleteBtn);

		let newRow = tbody.insertRow(-1);
		let i = 0;

		values.forEach(element => {
			let newCell = newRow.insertCell(i);

			if (typeof element == "object") {
				// create update button with link to updateform
				if (element.innerText == "Edit") {
					let a = document.createElement("a");
					a.setAttribute("href", `update?id=${res.results}`);

					newCell.appendChild(a);
					a.appendChild(element);

					// create delete button which calls delete AJAX request onclick
					// passing id of this particular row
				} else {
					let a = document.createElement("a");
					a.setAttribute("onClick", `deleteRequest(${res.results})`);

					newCell.appendChild(a);
					a.appendChild(element);
				}
			} else {
				newCell.textContent = element;
				newRow.setAttribute("id", res.results);
			}

			if (!element) newCell.textContent = 0;
			i++;
		});
	});

	req.send(JSON.stringify(data));
	e.preventDefault();
});

const deleteRequest = id => {
	for (let i of tbody.children) {
		let rowId = i.getAttribute("id");
		if (rowId == id) {
			i.parentNode.removeChild(i);
		}
	}

	// query backend with id to delete
	const req = new XMLHttpRequest();
	req.open("DELETE", `/?id=${id}`, true);
	req.send(`/?id=${id}`);
};
