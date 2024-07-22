
function show_password()
{
    logotag = document.getElementById('logo-eyes')
    password_tag = document.getElementById('password');
    console.log(logotag.className)
    if (password_tag.type === 'password')
    {
        password_tag.type = 'text'
        logotag.className = "bi bi-eye-slash"
    }
    else
    {
        password_tag.type = 'password'
        logotag.className = "bi bi-eye"
    }
}
