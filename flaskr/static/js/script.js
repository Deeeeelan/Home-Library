window.onload = async function () {

    window.dom={};
    document.querySelectorAll("[id]").forEach(el => window.dom[el.id] = el);

    async function search_books() {
        dom.book_container.innerHTML = "";
        const response = await fetch("/api/search?" + new URLSearchParams({
            zip_code: dom.zip_code.value,
            name: dom.book_name.value,
            author: dom.author_name.value,
        }).toString(), {
            method: "GET",
        })
        const result = await response.json();
        if (!result.success) {
            alert("Invalid");
            return
        }
        result.books.forEach((book) => {
            console.log(book)
            var book_el = document.createElement("div");
            book_el.innerHTML = `
                <h2 class="book_title">${book.name}</h2>
                <h3 class="author">${book.author}</h3>
                <p class="book_desc">${book.desc}</p>
                <button type="button" class="request_book">Request</button>`;
            dom.book_container.appendChild(book_el);
            book_el.querySelector("button").onclick = async function () {
                const response = await fetch("/api/book/" + book.id + "/checkout_req", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ jwt: localStorage.getItem("jwt"), 
                    }),
                })
		        const result = await response.json();
                if (result.success) {
                    alert("Requested Book!");
                    return
                }
            }
        })
    }

    console.log(window.dom);
    // dom.main_search_button.onclick = search_books;
    dom.filter_button.onclick = search_books;
};
