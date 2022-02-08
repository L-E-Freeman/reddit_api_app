function filterTable() {
    var upvoteInput = document.getElementById("upvoteinput").value
    table = document.getElementById("commenttable")

    // Loop iterates over iterable objects, in this case 
    // an HTMLCollection object table.rows - an array-like list of HTML 
    // elements.
    for (let row of table.rows) {
        let numUpvotes = parseInt(row.cells[1].innerText);
        if (numUpvotes < upvoteInput) {
            // clears filtered rows
            row.style.display = "none"
        } else {
            // resets list when input cleared.
            row.style.display = "";
        }
    }
}

