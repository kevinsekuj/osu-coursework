const btn = document.querySelector("button");

btn.addEventListener("click", function (e) {
	const req = new XMLHttpRequest();
	const data = { subject: null, message: null };

	data.subject = document.getElementById("subject").value;
	data.message = document.getElementById("textarea").value;

	req.open("POST", "https://httpbin.org/post", false);
	req.setRequestHeader("Content-Type", "application/json");

	req.send(JSON.stringify(data));
	const res = JSON.parse(req.responseText);
	const { subject, message } = res.json;

	// view POST response in console to view data transmission
	console.log(res);
	console.log(`Subject: ${subject}, Message: ${message}`);

	e.preventDefault();
	hideForm();
	alert(subject, message);
});

const hideForm = () => {
	const postForm = document.getElementById("formContainer");
	postForm.style.display = "none";
};
const alert = (subject, msg) => {
	const alertMsg = document.getElementById("alert");
	const header = document.getElementById("status");
	const message = document.getElementById("message");

	alertMsg.style.visibility = "visible";
	header.textContent = `Subject: ${subject}`;
	message.textContent = `Message body: ${msg}`;
};
