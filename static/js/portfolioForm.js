"use strict";

console.log("JavaScript is working!");

window.addEventListener('load', function () {
        var forms = document.getElementsByClassName('needs-validation');
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);

//document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("contactForm");
    const formMessage = document.getElementById("formMessage");

    form.addEventListener("submit", function(evt) {
        evt.preventDefault();

        let name = document.getElementById("name").value;
        let email = document.getElementById("email").value;
        let message = document.getElementById("message").value;

        //validation part
        let namePat = /^[A-za-z\s]+$/;
        if (!namePat.test(name)) {
            formMessage.textContent = "Name can only contain letters"
            formMessage.style.color = 'red';
            return;
        }

        //validate emails
        let emailPat = /[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$/;
        if (!email.includes("@")) {
            formMessage.textContent = "Email must contain '@'.";
            formMessage.style.color = "red";
            return;
        }

        if (message.trim() === "") {
            formMessage.textContent = "Message cannot be empty.";
            formMessage.style.color = "red";
            return;
        }

        formMessage.textContent = "Success! Your message has been sent.";
        formMessage.style.color = "green";
    })
//});
console.log("End of JS");