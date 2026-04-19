console.log("js is running")

function search_books() {
    console.log("searching")
    const response = fetch("http://127.0.0.1:5000/api/search", {
        method: "GET",
        body: JSON.stringify({ zip_code: "01234" }),
    })
    console.log(response)
}