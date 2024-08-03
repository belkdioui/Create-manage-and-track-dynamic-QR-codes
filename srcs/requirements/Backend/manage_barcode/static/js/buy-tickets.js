

function decr_incre(value, id, operation)
{
    var element = document.getElementById(id);
    var total_1 = document.getElementById("total_1");
    var total_2 = document.getElementById("total_2");
    var total_3 = document.getElementById("total_3");
    var number_of_free_ticket;

    if(operation == "+" && element.value < 100){
        if(id == "input_1")
        {
            element.value = parseInt(element.value) + value;
            total_1.innerHTML=element.value * 5;
        }
        if(id == "input_2")
        {
            element.value = parseInt(element.value) + value + 2;
            number_of_free_ticket  = (element.value / 12)*2;
            total_2.innerHTML=(element.value - number_of_free_ticket) * 5;
        }
        if(id == "input_3")
        {
            element.value = parseInt(element.value) + value + 5;
            number_of_free_ticket  = (element.value / 25)*5;
            total_3.innerHTML=(element.value - number_of_free_ticket) * 5;
        }
    }
    else if (operation == "-"){
        if(id == "input_1" && element.value > 1)
        {
            element.value = parseInt(element.value) - value;
            total_1.innerHTML=((element.value) * 5);
        }
        if(id == "input_2" && element.value > 13)
        {
            element.value = parseInt(element.value) - value - 2;
            number_of_free_ticket  = (element.value / 12)*2;
            total_2.innerHTML=(element.value - number_of_free_ticket) * 5;
        }
        if(id == "input_3" && element.value > 25)
        {
            element.value = parseInt(element.value) - value - 5;
            number_of_free_ticket  = (element.value / 25)*5;
            total_3.innerHTML=(element.value - number_of_free_ticket) * 5;
        }
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function post_data(tick, total) {
    var tickets = document.getElementById(tick).value;
    var total_cash = document.getElementById(total).innerText;
    const csrfToken = getCookie('csrftoken');
    const data = {
        tickets_t: tickets,
        total_c: total_cash
    };
    showSpinner();
    fetch('/buy-tickets/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('.budget').innerText = data.balance;
        document.querySelector('.tickets').innerText = data.count_ticket;
        hideSpinner();
    })
    .catch(error => console.error('Error:', error));
}

function showSpinner() {
    spiner = document.getElementById("spinner-overlay").classList.add('active');
}

function hideSpinner() {
    spiner = document.getElementById("spinner-overlay").classList.remove('active');
}






// const notifications = document.querySelector(".notifications"),
// buttons = document.querySelectorAll(".buttons .btn");
// const toastDetails = {
//     timer: 10000,
//     success: {
//         icon: 'fa-circle-check',
//         text: 'Success: This is a success toast.',
//     },
//     error: {
//         icon: 'fa-circle-xmark',
//         text: 'Error: This is an error toast.',
//     },
//     warning: {
//         icon: 'fa-triangle-exclamation',
//         text: 'Warning: This is a warning toast.',
//     },
//     info: {
//         icon: 'fa-circle-info',
//         text: 'Info: This is an information toast.',
//     }
// }

// const removeToast = (toast) => {
//     toast.classList.add("hide");
//     if(toast.timeoutId) clearTimeout(toast.timeoutId);
//     setTimeout(() => toast.remove(), 10000);
// }

// const createToast = (id) => {
//     const { icon, text } = toastDetails[id];
//     const toast = document.createElement("li");
//     toast.className = `toast_1 ${id}`;
//     toast.innerHTML = `<div class="column">
//                          <i class="fa-solid ${icon}"></i>
//                          <span>${text}</span>
//                       </div>
//                       <i class="fa-solid fa-xmark" onclick="removeToast(this.parentElement)"></i>`;
//     notifications.appendChild(toast);
//     toast.timeoutId = setTimeout(() => removeToast(toast), toastDetails.timer);
// }

// buttons.forEach(btn => {
//     btn.addEventListener("click", () => createToast(btn.id));
// });