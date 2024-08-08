
buytickets = document.getElementById("buytickets").classList.remove('active');
home = document.getElementById("home").classList.remove("active");
schedulesstop = document.getElementById("Schedules_Stops").classList.add("active");
profil = document.getElementById("profile").classList.remove("active");



function change_dir()
{

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

