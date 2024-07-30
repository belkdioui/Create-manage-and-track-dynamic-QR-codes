function change_nav_stat()
{
    var name = window.location.pathname;
    console.log(name)
    if (name.includes("profile"))
        name = 'profile'
    if (name.includes("home"))
        name = 'home'
    if (name.includes("Buy_ticket"))
        name = 'Buy_ticket'
    if (name.includes("Time_Way"))
        name = 'Time_Way'

    doc = document.getElementById('profile');
    console.log(doc);

}

change_nav_stat()
