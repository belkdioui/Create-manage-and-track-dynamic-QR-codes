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
}

