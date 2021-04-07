const form = document.querySelector("form");
const inputs = document.querySelectorAll("input:not(#submit)");
form.addEventListener("submit", (e) => {
  e.preventDefault();
});

inputs.forEach((input) => {
  input.addEventListener("change", (e) => {
    if (e.target.value !== "") {
      document
        .querySelector(`label[for="${e.target.id}"]`)
        .classList.add("hid");
    } else {
      document
        .querySelector(`label[for="${e.target.id}"]`)
        .classList.remove("hid");
    }
  });
});
