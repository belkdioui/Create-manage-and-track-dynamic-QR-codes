

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
        console.log(data);
        document.querySelector('.budget').innerText = data.balance;
        document.querySelector('.tickets').innerText = data.count_ticket;
    })
    .catch(error => console.error('Error:', error));
}
