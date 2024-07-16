onFieldBlur = e => {
    if (!e.checkValidity()) {
      e.nextElementSibling.style = { display: "block" };
      e.style.border = "solid 1px red";
    } else {
      e.nextElementSibling.style.display = "none";
      e.style.border = "solid 1px black";
    }
  };
  onSubmit = $event => {
    alert("submitted");
    return false;
  };

  onReset = () => {
    alert("Reset");
  };