
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

  const fileInput = document.getElementById("file-upload");
  console.log(fileInput)
  const imageOutput = document.getElementById("icon_photo");

  fileInput.addEventListener("change", async () => {
    console.log("ana f event lisner")
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
  })
