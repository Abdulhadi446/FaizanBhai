// Save the content of the table to the Flask backend
function saveTable(tableName) {
    // Table element IDs are constructed as "<tableName>Table"
    let tableId = tableName + "Table";
    let table = document.getElementById(tableId);
    let rows = table.getElementsByTagName("tr");
    let tableData = [];

    // Iterate over each row
    for (let i = 0; i < rows.length; i++) {
        let cells = rows[i].getElementsByTagName("td");
        let rowData = [];
        // Only add rows with cells
        if (cells.length > 0) {
            for (let j = 0; j < cells.length; j++) {
                rowData.push(cells[j].innerText.trim());
            }
            tableData.push(rowData);
        }
    }
    
    // Send the updated table data to the Flask update route
    fetch("/update/" + tableName, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: tableData })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}