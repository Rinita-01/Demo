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

function validateusername(event) {
    const usernameField = event.target; // Get the input field
    const usernameValue = usernameField.value; // Get the value of the input field
    const regex = /^[a-zA-Z0-9_ ]{4,20}$/; // Regex to check the username pattern
    const errorspan = document.getElementById("username_error");

    // Check if the username value matches the regex
    if (!regex.test(usernameValue)) {
        errorspan.textContent = "Only letters, numbers, and underscore. Min 4 chars. eg. Abcde_7";
        return false;
    }

    // Clear the error message if valid
    errorspan.textContent = "";
    return true;
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

function validatepassword(event) {
    const passwordField = event.target;
    const errorspan = document.getElementById("password_error");
    const regex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

    if (passwordField.value.trim() === "") {
        errorspan.textContent = "";
        return true;
    }

    if (!regex.test(passwordField.value)) {
        errorspan.textContent = "Password must be at least 8 characters, including letters and numbers.";
        return false;
    }

    errorspan.textContent = "";
    return true;
}

// Attach the function to run every time the user types
document.getElementById("password").addEventListener("input", validatepassword);


