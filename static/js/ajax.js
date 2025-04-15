$(document).ready(function () {
    // AJAX for Registration
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

    // AJAX for Login
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
    
        const amount = parseFloat($('#amount').val());
        const book_id = $("input[name='book_id']").val();
        const category_id = $("input[name='category_id']").val();
        const quantity = $("input[name='quantity']").val();
    
        if (isNaN(amount) || amount <= 0) {
            alert('Please enter a valid amount.');
            return;
        }
    
        const amountInPaise = Math.round(amount * 100); // Convert to paise (integer)
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    
        console.log("Amount in paise: ", amountInPaise);
        console.log("CSRF Token: ", csrfToken);
    
        // Create Razorpay order via AJAX
        $.ajax({
            url: '/payments/create_order/',
            type: 'POST',
            data: {
                amount: amountInPaise.toString(),  // Send as string to avoid decimal issues
                book_id: book_id,
                category_id: category_id,
                quantity: quantity,
                csrfmiddlewaretoken: csrfToken
            },
            success: function (data) {
                console.log("API Response: ", data);
    
                const options = {
                    key: data.key,
                    amount: data.amount,
                    order_id: data.order_id,
                    currency: 'INR',
                    name: 'BuyBook Payments',
                    description: 'Payment for your order',
                    handler: function (response) {
                        alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
                        console.log("Payment Response: ", response);
    
                        // Verify the payment on server
                        $.ajax({
                            url: '/payments/verify_payment/',
                            type: 'POST',
                            data: {
                                razorpay_order_id: response.razorpay_order_id,
                                razorpay_payment_id: response.razorpay_payment_id,
                                razorpay_signature: response.razorpay_signature,
                                book_id: book_id,
                                category_id: category_id,
                                quantity: quantity,
                                amount: amount,
                                csrfmiddlewaretoken: csrfToken
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

    // Proceed to payment button click event
    $("#proceed-to-pay-btn").click(function (event) {
        event.preventDefault();

        const csrfToken = $("#csrf-token").val();
        const amount = $("#amount-input").val();

        if (!amount || parseFloat(amount) <= 0) {
            alert("Invalid amount.");
            return;
        }

        // Create a hidden form and submit it with POST
        const form = $('<form>', {
            method: 'POST',
            action: '/payments/payment/'  // Adjust this if your URL name is different
        });

        // CSRF token
        form.append($('<input>', {
            type: 'hidden',
            name: 'csrfmiddlewaretoken',
            value: csrfToken
        }));

        // Amount
        form.append($('<input>', {
            type: 'hidden',
            name: 'amount',
            value: amount
        }));

        $('body').append(form);
        form.submit();
    });
});

$(document).ready(function () {
    const quantitySelect = $('#quantity');
    const priceElement = $('#book-price');
    const totalPriceElement = $('#total-price');

    // Update total price when quantity changes
    quantitySelect.change(function () {
        const quantity = parseInt($(this).val());
        const unitPrice = parseFloat(priceElement.text());

        if (!isNaN(quantity) && !isNaN(unitPrice)) {
            const total = (quantity * unitPrice).toFixed(2);
            totalPriceElement.text(total);
        } else {
            totalPriceElement.text('0.00');
        }
    });

    // Handle Place Order + Payment Redirection
    $("#go-to-payment-btn").click(function (event) {
        event.preventDefault();
    
        const quantity = $("#quantity").val();
        const bookId = $("input[name='book_id']").val();
        const categoryId = $("input[name='category_id']").val();
        const csrfToken = $("input[name='csrfmiddlewaretoken']").val();
        const price = parseFloat($("#book-price").text());
    
        if (!quantity) {
            alert("Please select a quantity.");
            return;
        }
    
        const total = (price * quantity).toFixed(2);
    
        $.ajax({
            type: "POST",
            url: `/order/order_form/${bookId}/${categoryId}/`,
            data: {
                quantity: quantity,
                total_price: total,
                csrfmiddlewaretoken: csrfToken
            },
            success: function (response) {
                if (response.status === "success") {
                    alert("Order placed successfully! Redirecting to payment...");
    
                    // Dynamic POST form creation for secure redirection
                    const form = $('<form>', {
                        method: 'POST',
                        action: '/order/payment/'
                    });
    
                    form.append($('<input>', {
                        type: 'hidden',
                        name: 'csrfmiddlewaretoken',
                        value: csrfToken
                    }));
                    form.append($('<input>', {
                        type: 'hidden',
                        name: 'amount',
                        value: response.total_price
                    }));
                    form.append($('<input>', {
                        type: 'hidden',
                        name: 'book_id',
                        value: response.book_id
                    }));
                    form.append($('<input>', {
                        type: 'hidden',
                        name: 'category_id',
                        value: response.category_id
                    }));
                    form.append($('<input>', {
                        type: 'hidden',
                        name: 'quantity',
                        value: response.quantity
                    }));
    
                    $('body').append(form);
                    form.submit();
    
                } else {
                    alert(response.message || "Something went wrong.");
                }
            },
            error: function (xhr) {
                alert("Error: " + (xhr.responseJSON?.message || "Unexpected error"));
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll("#star-rating .star");
    const ratingInput = document.getElementById("rating");

    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            const rating = index + 1;
            ratingInput.value = rating;

            // Reset all
            stars.forEach(s => s.classList.remove('fa-star', 'text-warning'));
            stars.forEach(s => s.classList.add('fa-star-o'));

            // Highlight selected
            for (let i = 0; i < rating; i++) {
                stars[i].classList.remove('fa-star-o');
                stars[i].classList.add('fa-star', 'text-warning');
            }
        });
    });

    // AJAX submit
    $('#submit-button').click(function (event) {
        event.preventDefault();
    
        const rating = $('#rating').val();
        const comment = $('#comment').val();
        const bookId = $(this).data('book-id');
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    
        if (!rating || !comment) {
            $('#message').html(`<div class="alert alert-danger">Please fill all fields.</div>`);
            return;
        }
    
        $.ajax({
            url: `/reviews/submit/${bookId}/`,
            method: "POST",
            data: {
                rating: rating,
                comment: comment,
                csrfmiddlewaretoken: csrfToken
            },
            success: function (response) {
                $('#message').html(`<div class="alert alert-success">${response.message}</div>`);
    
                $('#review-form')[0].reset();
                $('#rating').val('');
                $(".star").removeClass("fa-star text-warning").addClass("fa-star-o");
    
                const stars = '★'.repeat(response.review.rating) + '☆'.repeat(5 - response.review.rating);
    
                const newReviewHtml = `
                    <div class="card mt-3">
                        <div class="card-body">
                            <strong>${response.review.username}</strong><br>
                            <span class="text-warning">${stars}</span>
                            <p class="mt-2">${response.review.comment}</p>
                        </div>
                    </div>
                `;
                $('#review-section').prepend(newReviewHtml);
            },
            error: function (xhr) {
                let errorMsg = "Something went wrong. Please try again.";
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                }
                $('#message').html(`<div class="alert alert-danger">${errorMsg}</div>`);
            }
        });
    });
});
