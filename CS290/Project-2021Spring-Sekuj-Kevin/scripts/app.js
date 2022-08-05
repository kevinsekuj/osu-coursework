const splash = document.querySelector(".splash");
document.addEventListener("DOMContentLoaded", e => {
	setTimeout(() => {
		splash.classList.add("hidden");
	}, 3500);
});

const container = document.querySelector(".typing");
const text = ["YUNG LEAN", "JONATAN LEANDOER", "ЮНАТАН ЛЕАНДЁР"];
let i = 0;

const type = async str => {
	let p = document.createElement("p");
	for (let i = 0; i < str.length; i++) {
		await new Promise(res => setTimeout(res, 75));
		p.innerHTML += str[i];
		container.appendChild(p);
	}
};

const log = async arr => {
	for (let el of arr) {
		await type(el);
	}
};
log(text);
