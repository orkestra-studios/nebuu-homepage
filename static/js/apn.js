function invalidate() {
  var confirm = document.getElementById("confirm");
  var submit = document.getElementById("submit");
  confirm.checked = false;
  submit.disabled = true;
  submit.classList.add("disabled")
}

function validate() {
  var confirm = document.getElementById("confirm");
  var submit = document.getElementById("submit");
  submit.disabled = confirm.checked;
  console.log("validate");
  if (confirm.checked) {
    submit.classList.add("disabled")
  } else {
    submit.classList.remove("disabled")
    populate();
  }
}

function populate() {
  var title = document.getElementById("title");
  var body  = document.getElementById("body");

  var ce_title = document.getElementById("ce-title");
  var ce_body  = document.getElementById("ce-body");

  title.value = ce_title.innerHTML;
  body.value  = ce_body.innerHTML;
  console.log("populate");
}
