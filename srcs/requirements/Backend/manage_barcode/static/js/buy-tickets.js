

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
