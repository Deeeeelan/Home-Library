window.onload = async function () {

	window.dom={};
	document.querySelectorAll("[id]").forEach(el => window.dom[el.id] = el);

	async function submit() {
		const response = await fetch("/api/login", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ username: dom.username.value, password: dom.password.value})
		});
		const result = await response.json();
		if (!result.success) {
			alert("Wrong username or password");
			return
		}
        localStorage.setItem("jwt", result.jwt)
        window.location.assign("/")

	}

	dom.login_button.onclick = submit;
};

