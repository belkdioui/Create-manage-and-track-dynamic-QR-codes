
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
    const imageOutput = document.getElementById("avatar_photo");

    fileInput.addEventListener('change', (event) => {
      if (event.target.files.length > 0)
      {
        let file = fileInput.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
              console.log("ana f onload")
              imageOutput.src = e.target.result;
        };
        reader.onerror = (err) => {
                console.error("Error reading file:", err);
                alert("An error occurred while reading the file.");
            };
            reader.readAsDataURL(file);
      }
    });
}


function edit_data()
{
  data_div = document.getElementsByClassName("data-account");
  for (let i = 0; i < data_div.length; i++)
  {
    const inputs = data_div[i].querySelector('input');
    if (inputs.disabled == true)
      inputs.disabled=false;
    else
      inputs.disabled = true;
  }
}

function delete_account()
{
  const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

  fetch("/delete_account/",
  {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
  },
  }).then(response => {
    if(!response.ok) {
        return response.json().then(data => {
            if(response.status == 200){
                createToast('success', "account has been deleted");
            }
            else{
                createToast('error', 'No user to be deleted');
            }
        })
    }
    return response.json();
})
.catch(error => console.error('Error:', error));
}