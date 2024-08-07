
function togglePasswordVisibility() {
    const passwordInput = document.getElementById('Password');
    const toggleIcon = document.getElementById('toggle-icon');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('bi-eye');
        toggleIcon.classList.add('bi-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('bi-eye-slash');
        toggleIcon.classList.add('bi-eye');
    }
}


// function signup_btn_funct()
// {
//     {% for field, field_errors in errors.items %}
//     <div style="color: white">
//       {{field_errors}}
//     </div>
//     {%endfor%}
//     // console.log("hereeee");
//     createToast("success", "verifay your email");
// }

