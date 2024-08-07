function change_dir()
{
    console.log("here");

    terminusX = document.getElementById('terminusX');
    terminusY = document.getElementById('terminusY');
    first_child_of_td = document.getElementById('first_child_of_td');

    temp = terminusX.innerHTML;
    terminusX.innerHTML = terminusY.innerHTML;
    first_child_of_td.innerHTML = terminusY.innerHTML;
    terminusY.innerHTML = temp;

    const table = document.getElementById('data-table');
    const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
    for (let row of rows) {
        const cells = Array.from(row.getElementsByTagName('td'));
        cells.reverse();
        row.innerHTML = '';
        for (let cell of cells) {
            row.appendChild(cell);
        }
    }
}

