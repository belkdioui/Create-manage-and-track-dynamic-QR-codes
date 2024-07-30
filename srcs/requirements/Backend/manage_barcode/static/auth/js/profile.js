
function reclick()
{
    console.log("clickerrrrr")
    document.getElementById('file-upload').click();
    displayit()
}
function displayit()
{
    const fileInput = document.getElementById('file-upload');
    const submitButton = document.getElementById('save_button1');

    fileInput.addEventListener('change', (event) => {
    if (event.target.files.length > 0) {
     submitButton.disabled = false;
    } else {
    submitButton.disabled = true;
  }
    });
}