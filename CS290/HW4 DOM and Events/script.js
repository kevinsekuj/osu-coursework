const body = document.querySelector("body");
const table = document.createElement("table");
const tbody = document.createElement("tbody");
const thead = document.createElement("thead");

body.appendChild(table);
table.appendChild(thead);

// loop to create headers
const createHeader = () => {
	const tr = document.createElement("tr");
	for (let i = 0; i < 4; i++) {
		const th = document.createElement("th");
		th.textContent = `Header ${i + 1}`;
		tr.appendChild(th);
	}

	thead.appendChild(tr);
	table.appendChild(tbody);
};

// create three rows, appending four td elements each
const createCells = () => {
	for (let i = 0; i < 3; i++) {
		const tr = document.createElement("tr");
		for (let j = 0; j < 4; j++) {
			const td = document.createElement("td");
			td.textContent = `${i + 1}, ${j + 1}`;
			tr.appendChild(td);
		}

		tbody.appendChild(tr);
	}
};

createHeader();
createCells();

const titles = ["up", "down", "left", "right", "Mark Cell"];

// generate button func, takes title param and sets to button text and id
const createButton = title => {
	let button = document.createElement("button");
	button.setAttribute("id", title.split(" ").join("").toLowerCase());
	button.textContent = title;
	return button;
};

// call createButton on each title in titles array to create 5 buttons
titles.forEach(el => body.appendChild(createButton(el)));

// index through td NodeList and set backgrounds
const cells = document.querySelectorAll("td");

for (let cell of cells) {
	cell.style.border = "1px dotted";
}

let i = 0;
cells[i].style.border = "2px solid";

const up = document.getElementById("up"),
	down = document.getElementById("down"),
	left = document.getElementById("left"),
	right = document.getElementById("right"),
	markcell = document.getElementById("markcell");

// takes integer param on click and add to cells index
// to simulate table cell movement, changing background with moves
const moveCell = int => {
	cells[i].style.border = "1px dotted";
	i += int;
	cells[i].style.border = "2px solid";
};

// event listeners
up.addEventListener("click", function () {
	if (i - 4 < 0) {
		console.log("Invalid move.");
	} else {
		moveCell(-4);
	}
});

down.addEventListener("click", function () {
	if (i + 4 > 11) {
		console.log("Invalid move.");
	} else {
		moveCell(4);
	}
});

right.addEventListener("click", function () {
	if (i === 3 || i === 7 || i === 11) {
		console.log("Invalid move.");
	} else {
		moveCell(1);
	}
});

left.addEventListener("click", function () {
	if (i === 0 || i === 4 || i === 8) {
		console.log("Invalid move.");
	} else {
		moveCell(-1);
	}
});

markcell.addEventListener("click", function () {
	cells[i].style.backgroundColor = "yellow";
});
