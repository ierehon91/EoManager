function filterTable(event) {
    const query = event.target.value.toLowerCase();
    const rows = tableBody.querySelectorAll('tr');

    rows.forEach(row => {
        const columns = row.querySelectorAll('td');
        let match = false;

        columns.forEach(column => {
            if (column.textContent.toLowerCase().includes(query)) {
                match = true;
            }
        });

        if (match) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}