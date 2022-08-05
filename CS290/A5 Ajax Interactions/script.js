document.addEventListener("DOMContentLoaded", bindButtons);

function bindButtons() {
	document
		.getElementById("getSubmit")
		.addEventListener("click", function (event) {
			let req = new XMLHttpRequest();
			let city = document.getElementById("city").value;
			let zip = document.getElementById("zip").value;
			let country = document.getElementById("country").value;

			// rubric: city + country code OR zip + country code

			if (city) {
				req.open(
					"GET",
					`http://api.openweathermap.org/data/2.5/weather?q=${city},${country}&appid=d96739423a322f39944c15947936643f`,
					true
				);
			} else if (zip) {
				req.open(
					"GET",
					`https://api.openweathermap.org/data/2.5/weather?zip=${zip},${country}&appid=d96739423a322f39944c15947936643f`,
					true
				);
			} else {
				alert("You must enter a city or zip code.");
			}

			req.addEventListener("load", function () {
				let response = JSON.parse(req.responseText);
				let weather = response.main.temp;
				console.log(weather);
				document.getElementById("form1Result").textContent = weather;
			});

			req.send(null);
			event.preventDefault();
		});

	document
		.getElementById("postsubmit")
		.addEventListener("click", function (event) {
			let req = new XMLHttpRequest();
			let payload = { userData: null };
			payload.userData = document.getElementById("usersubmit").value;

			req.open("POST", "http://httpbin.org/post", true);
			req.setRequestHeader("Content-Type", "application/json");

			req.addEventListener("load", function () {
				let res = JSON.parse(req.responseText);
				document.getElementById("form2Result").textContent =
					res.json.userData;
			});
			req.send(JSON.stringify(payload));
			event.preventDefault();
		});
}
