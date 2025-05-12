function validatefirstname(event){

    const regex = /^[a-zA-Z ]$/;
    const key = event.key;
    const errorspan = document.getElementById("first_name_error");

    if(!regex.test(key)) {
        event.preventDefault();
        errorspan.textContent = "only Alphabets, space are allowed";
        return false;

    }else{
        errorspan.textContent = "";
        return true;
    }    
}

function validatelastname(event){

    const regex = /^[a-zA-Z ]$/;
    const key = event.key;
    const errorspan = document.getElementById("last_name_error");

    if(!regex.test(key)) {
        event.preventDefault();
        errorspan.textContent = "only Alphabets, space are allowed";
        return false;

    }else{
        errorspan.textContent = "";
        return true;
    }    
}

function restrictUsername(input) {
    let cleaned = input.value.replace(/[^a-z0-9]/g, ""); // allow only a-z and 0-9
    input.value = cleaned;

    const errorSpan = document.getElementById("username_error");
    if (!/^[a-z]{4,}[0-9]*$/.test(cleaned)) {
      errorSpan.textContent = "Start with at least 4 lowercase letters. Numbers allowed after. Max 20 chars.";
    } else {
      errorSpan.textContent = "";
    }

    if (cleaned.length > 20) {
      input.value = cleaned.slice(0, 20); // limit to 20 characters
    }
}

function validatephone(event) {
    const regex = /^[0-9]{0,10}$/; // Allows up to 10 digits
    const inputField = event.target;
    const newValue = inputField.value + event.key; // Simulate new value after key press
    const errorspan = document.getElementById("phone_error");

    if (!/^[0-9]$/.test(event.key) && event.key !== "Backspace") {
        event.preventDefault();
        errorspan.textContent = "Only numbers are allowed.";
        return false;
    }

    if (!regex.test(newValue)) {
        event.preventDefault();
        errorspan.textContent = "Phone number cannot exceed 10 digits.";
        return false;
    }

    errorspan.textContent = "";
    return true;
}

function validateaddress(event) {
    const addressField = event.target; // Get the input field
    const addressValue = addressField.value; // Get the value of the input field
    const regex = /^.{5,}$/; // Regex to check if address length is at least 5 characters
    const errorspan = document.getElementById("address_error"); // Error message span

    // Check if the address is valid
    if (!regex.test(addressValue)) {
        errorspan.textContent = "Address must be at least 5 characters long.";
        return false;
    } else {
        errorspan.textContent = "";
        return true;
    }
}

function validateemail(event) {
    const emailField = event.target;
    const errorspan = document.getElementById("email_error");
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

    if (emailField.value.trim() === "") {
        errorspan.textContent = ""; // No error when field is empty
        return true;
    }

    if (!regex.test(emailField.value)) {
        errorspan.textContent = "Enter a valid email address.";
        return false;
    }

    errorspan.textContent = "";
    return true;
}

const passwordInput = document.querySelector(".pass-field input");
document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.getElementById("password");
    const eyeIcon = document.querySelector(".pass-field i");
    const requirementList = document.querySelectorAll(".requirement-list li");

    const requirements = [
        { regex: /.{8,}/, index: 0 },
        { regex: /[0-9]/, index: 1 },
        { regex: /[a-z]/, index: 2 },
        { regex: /[^A-Za-z0-9]/, index: 3 },
        { regex: /[A-Z]/, index: 4 },
    ];

    passwordInput.addEventListener("keyup", (e) => {
        const value = e.target.value;
        requirements.forEach(req => {
            const isValid = req.regex.test(value);
            const item = requirementList[req.index];
            if (isValid) {
                item.classList.add("valid");
                item.firstElementChild.className = "fa-solid fa-check";
            } else {
                item.classList.remove("valid");
                item.firstElementChild.className = "fa-solid fa-circle";
            }
        });
    });

    eyeIcon.addEventListener("click", () => {
        const type = passwordInput.type === "password" ? "text" : "password";
        passwordInput.type = type;
        eyeIcon.className = `fa-solid fa-eye${type === "password" ? "" : "-slash"}`;
    });
});