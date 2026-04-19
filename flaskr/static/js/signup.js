window.onload = async function () {

	window.dom={};
	document.querySelectorAll("[id]").forEach(el => window.dom[el.id] = el);

	async function submit() {
		const response = await fetch("/api/signup", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				username: dom.username.value,
				password: dom.password.value,
				display_name: dom.display_name.value,
				zip_code: dom.user_zip_code.value,
			})
		});
		const result = await response.json();
		if (!result.success) {
			alert("Invalid: " + result.error);
			return
		}
        localStorage.setItem("jwt", result.jwt)
        window.location.assign("/")

	}

	dom.signup_button.onclick = submit;
};

