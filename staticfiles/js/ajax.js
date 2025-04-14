$(document).ready(function () {
    $("#register-btn").click(function (event) {
        event.preventDefault(); // Prevent default button behavior
        
        let formData = new FormData();
        formData.append("email", $("#email").val().trim());
        formData.append("password", $("#password").val().trim());
        formData.append("first_name", $("#first_name").val().trim());
        formData.append("last_name", $("#last_name").val().trim());
        formData.append("username", $("#username").val().trim());
        formData.append("dob", $("#dob").val().trim());
        formData.append("gender", $("#gender").val());
        formData.append("phone", $("#phone").val().trim());
        formData.append("address", $("#address").val().trim());

        console.log(formData)
        
        let profilePicture = $("#profile_picture")[0].files[0]; // Get file
        if (profilePicture) {
            formData.append("profile_picture", profilePicture);
        }

        formData.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());

        $("#register-btn").prop("disabled", true); // Disable button

        $.ajax({
            type: "POST",
            url: "/users/register/",
            data: formData,
            processData: false,
            contentType: false,
            dataType: "json",
            success: function (response) {
                if (response.success) {
                    alert("Registration successful! Redirecting to login...");
                    window.location.assign("/users/customer_login/");
                } else {
                    alert("Error: " + response.error);
                }
            },
            error: function () {
                alert("Something went wrong. Please try again.");
            },
            complete: function () {
                $("#register-btn").prop("disabled", false);
            }
        });
    });


    $("#login-btn").click(function (event) {
        event.preventDefault(); // Prevent default form submission
    
        let email = $("#email").val().trim();
        let password = $("#password").val().trim();
    
        if (!email || !password) {
            alert("Please enter both email and password.");
            return;
        }
    
        $("#login-btn").prop("disabled", true); // Disable button to prevent multiple clicks
    
        $.ajax({
            type: "POST",
            url: "/users/customer_login/",
            data: {
                email: email,
                password: password,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: "json",
            success: function (response) {
                if (response.success) {
                    alert("Login successful! Redirecting...");
                    window.location.assign(response.redirect_url);
                } else {
                    alert("Error: " + response.error);
                }
            },
            error: function (xhr, status, error) {
                alert("Something went wrong. Please try again.");
                console.log("AJAX error:", xhr.responseText);
            },
            complete: function () {
                $("#login-btn").prop("disabled", false);
            }
        });
    });
    
    // AJAX for Add to Cart
    $("#add-to-cart-btn").click(function (event) {
        event.preventDefault(); // Prevent default form submission

        var book_id = $("input[name='prod_id']").val();
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val(); // Get CSRF token

        $.ajax({
            url: "/cart/add_to_cart/",
            type: "POST",
            data: {
                prod_id: book_id,
                csrfmiddlewaretoken: csrf_token // Include CSRF token
            },
            success: function (response) {
                alert(response.message); // Show success message
                $("#cart-count").text(response.total_item); // Update cart count in navbar
            },
            error: function (xhr) {
                alert("Error: " + xhr.responseJSON.message);
            }
        });
    });

    function updateSummary(response) {
        $("#amount").text(response.amount.toFixed(2));  // Update subtotal
        $("#totalamount").text(response.total_amount.toFixed(2));  // Update total
    }
    
    // Increase Quantity
    $(".plus-cart").click(function () {
        let book_id = $(this).attr("pid");
        let quantityElement = $(this).siblings("#quantity");
    
        $.ajax({
            type: "GET",
            url: "/cart/update/",
            data: {
                book_id: book_id,
                action: "increase"
            },
            success: function (response) {
                if (response.success) {
                    quantityElement.text(response.quantity);
                    updateSummary(response);
                }
            },
            error: function () {
                alert("Something went wrong!");
            }
        });
    });
    
    // Decrease Quantity
    $(".minus-cart").click(function () {
        let book_id = $(this).attr("pid");
        let quantityElement = $(this).siblings("#quantity");
    
        $.ajax({
            type: "GET",
            url: "/cart/update/",
            data: {
                book_id: book_id,
                action: "decrease"
            },
            success: function (response) {
                if (response.success) {
                    if (response.quantity === 0) {
                        location.reload(); // Reload if item is removed
                    } else {
                        quantityElement.text(response.quantity);
                        updateSummary(response);
                    }
                }
            },
            error: function () {
                alert("Something went wrong!");
            }
        });
    });
    

    // Remove Item from Cart
    $(".remove-cart").click(function () {
        let book_id = $(this).attr("pid");

        $.ajax({
            type: "GET",
            url: "/cart/remove/",
            data: {
                book_id: book_id
            },
            success: function (response) {
                if (response.success) {
                    location.reload(); // Reload the cart if item is removed
                }
            },
            error: function () {
                alert("Failed to remove item. Please try again.");
            }
        });
    });

    // Checkout button click event
    $('#pay-button').click(function (event) {
        event.preventDefault();
        const amount = $('#amount').val();
    
        if (!amount || amount <= 0) {
          alert('Please enter a valid amount.');
          return;
        }

        console.log("Amount: ", amount);
        console.log("CSRF Token: ", $('input[name="csrfmiddlewaretoken"]').val());
    
        // AJAX request to create an order
        $.ajax({
            url: '/payment/create-order/',
            type: 'POST',
            data: {
                amount: amount,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() // Include CSRF token
            },
            success: function (data) {
                console.log("API Response: ", data);  // Check response in console

                const options = {
                    key: data.key,
                    amount: data.amount,
                    order_id: data.order_id, // Use the order_id returned from the server
                    currency: 'INR',
                    name: 'BuyBook Payments',
                    description: 'Payment for your order',
                    
                    handler: function (response) {
                        alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
                        console.log("Payment Response: ", response); 

                        // Sending the payment details to your server for verification
                        $.ajax({
                            url: '/payment/verify-payment/',
                            type: 'POST',
                            data: {
                                razorpay_order_id: response.razorpay_order_id,
                                razorpay_payment_id: response.razorpay_payment_id,
                                razorpay_signature: response.razorpay_signature,
                                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                            },
                            success: function (verificationResponse) {
                                if (verificationResponse.success) {
                                    alert("Payment verified successfully!");
                                } else {
                                    alert("Payment verification failed: " + verificationResponse.error);
                                }
                            },
                            error: function (error) {
                                alert("Error verifying payment.");
                                console.error(error);
                            }
                        });
                    }
                };

                const rzp = new Razorpay(options);
                rzp.open();
            },
            error: function (error) {
                console.error('Order creation error:', error);
                alert('Error creating order.');
            }
        });
    });
});


$(document).ready(function(){
    $("#admin-Register-btn").click(function(event){
        event.preventDefault();

        var formData = new FormData();
        formData.append("username", $("#username").val());
        formData.append("email", $("#email").val());
        formData.append("password", $("#password").val());
        formData.append("first_name", $("#first_name").val());
        formData.append("last_name", $("#last_name").val());
        formData.append("dob", $("#dob").val());
        formData.append("gender", $("#gender").val());
        formData.append("phone", $("#phone").val());
        formData.append("address", $("#address").val());
        let profilePicture = $("#profile_picture")[0].files[0]; // Get file
        if (profilePicture) {
            formData.append("profile_picture", profilePicture);
        }

        // Retrieve CSRF token from meta tag
        formData.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());

        $.ajax({
            url: "/users/admin_registration/",  // Ensure this is correct
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            dataType: "json",
            success: function(response) {
                if (response.success) {
                    $("#message").text(response.message).css("color", "green");
                    setTimeout(function() {
                        window.location.href = response.redirect_url;  // Redirect after registration
                    }, 2000);
                } else {
                    $("#message").text(response.error).css("color", "red");
                }
            },
            error: function(response) {
                var errorMsg = response.responseJSON?.error || "An error occurred";
                $("#message").text(errorMsg).css("color", "red");
            }
        });
    });
});


// document.addEventListener('DOMContentLoaded', function () {
//     const quantitySelect = document.getElementById('quantity');
//     const priceElement = document.getElementById('book-price');
//     const totalPriceElement = document.getElementById('total-price');
//     const addOrderBtn = document.getElementById('add-order-btn');

//     quantitySelect.addEventListener('change', function () {
//         const quantity = parseInt(this.value);
//         const unitPrice = parseFloat(priceElement.textContent);

//         if (!isNaN(quantity) && !isNaN(unitPrice)) {
//             const total = (quantity * unitPrice).toFixed(2);
//             totalPriceElement.textContent = total;
//         } else {
//             totalPriceElement.textContent = '0.00';
//         }
//     });

//     addOrderBtn.addEventListener('click', function (event) {
//         event.preventDefault();

//         const bookId = $("input[name='book_id']").val();
//         const categoryId = $("input[name='category_id']").val();
//         const quantity = $("#quantity").val();
//         const csrfToken = $("input[name='csrfmiddlewaretoken']").val();
//         const totalPrice = $("#total-price").text();

//         if (!quantity) {
//             alert("Please select a quantity.");
//             return;
//         }

//         $.ajax({
//             type: "POST",
//             url: `/order/order_form/${bookId}/${categoryId}/`,
//             data: {
//                 quantity: quantity,
//                 total_price: totalPrice,
//                 csrfmiddlewaretoken: csrfToken
//             },
//             success: function (response) {
//                 if (response.status === "success") {
//                     alert(response.message);
//                     window.location.href = response.redirect_url;
//                 } else {
//                     alert(response.message);
//                 }
//             },
//             error: function (xhr) {
//                 alert("Error: " + xhr.responseJSON.message);
//             }
//         });
//     });
// });

