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
        event.preventDefault();
    
        var book_id = $("input[name='prod_id']").val();
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    
        $.ajax({
            url: "/cart/add_to_cart/",
            type: "POST",
            data: {
                prod_id: book_id,
                csrfmiddlewaretoken: csrf_token
            },
            success: function (response) {
                alert(response.message);
                $("#cart-count").text(response.total_item);
            },
            error: function (xhr) {
                alert("Error: " + (xhr.responseJSON?.message || "Unexpected error"));
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

    // AJAX for Payment
    $('#pay-button').click(function (event) {
        event.preventDefault();
    
        const amount = parseFloat($('#amount').val().trim());
        const book_id = $("input[name='book_id']").val()?.trim();
        const category_id = $("input[name='category_id']").val()?.trim();
        const quantity = parseInt($("input[name='quantity']").val()?.trim()) || 1;
    
        if (isNaN(amount) || amount <= 0) {
            alert('Please enter a valid amount.');
            return;
        }
    
        const amountInPaise = Math.round(amount * 100);
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    
        // Prepare data for order creation
        let requestData = {
            amount: amountInPaise.toString(),
            csrfmiddlewaretoken: csrfToken
        };
    
        // Include book details if it's a direct "Buy Now" purchase
        if (book_id && category_id) {
            requestData.book_id = book_id;
            requestData.category_id = category_id;
            requestData.quantity = quantity;
        }
    
        // Create Razorpay order
        $.ajax({
            url: '/payments/create_order/',
            type: 'POST',
            data: requestData,
            success: function (data) {
                const options = {
                    key: data.key,
                    amount: data.amount,
                    order_id: data.order_id,
                    currency: 'INR',
                    name: 'BuyBook Payments',
                    description: 'Payment for your order',
                    handler: function (response) {
                        alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
    
                        // Prepare data for server-side payment verification
                        let verifyData = {
                            razorpay_order_id: response.razorpay_order_id,
                            razorpay_payment_id: response.razorpay_payment_id,
                            razorpay_signature: response.razorpay_signature,
                            csrfmiddlewaretoken: csrfToken
                        };
    
                        if (book_id && category_id) {
                            verifyData.book_id = book_id;
                            verifyData.category_id = category_id;
                            verifyData.quantity = quantity;
                            verifyData.amount = amount;
                        }
    
                        // Verify the payment
                        $.ajax({
                            url: '/payments/verify_payment/',
                            type: 'POST',
                            data: verifyData,
                            success: function (verificationResponse) {
                                if (verificationResponse.success) {
                                    alert("Payment verified successfully!");
                                    window.location.href = `/payments/order_success/${verificationResponse.order_id}/`;
                                } else {
                                    alert("Payment verification failed: " + verificationResponse.error);
                                }
                            },
                            error: function (error) {
                                console.error("Verification error:", error);
                                alert("Error verifying payment.");
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
    
    
    $("#proceed-to-pay-btn").click(function (event) {
        event.preventDefault();
        console.log("Proceed to payment button clicked");

        const quantity = $("#quantity").text();  // or `.val()` if it's an input
        const csrfToken = $("#csrf-token").val();
        const price = parseFloat($("#amount").text());  // Or any total price shown
        const shipping = 70.00;
        const total = (price + shipping).toFixed(2);
        console.log("Total amount: ", total);
    
        $.ajax({
            type: "POST",
            url: `/order/order_form_cart/`,
            data: {
                quantity: quantity,
                total_price: total,
                csrfmiddlewaretoken: csrfToken
            },
            success: function (response) {
                if (response.status === "success") {
                    // Dynamic POST form for secure payment redirection
                    const form = $('<form>', {
                        method: 'POST',
                        action: '/cart/payment/'
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

    // AJAX for Cart Item Selection
    $('input[name="selected_items"]').on('change', function() {
        let cartId = $(this).val();
        let isChecked = $(this).is(':checked');
        let csrfToken = $('#csrf-token').val();
    
        $.ajax({
            url: `/cart/toggle-cart-item/`,
            method: "POST",
            data: {
                cart_id: cartId,
                is_active: isChecked,
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                console.log(response.message);
                
                // 🟢 After updating item status, fetch the new totals
                $.ajax({
                    url: "/cart/totals/",
                    method: "GET",
                    success: function(data) {
                        $('#amount').text(data.amount);
                        $('#totalamount').text(data.total_amount);
                    }
                });
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    });
            
});

// AJAX for Book Details
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
    
        const total = (price * quantity + 70).toFixed(2);
    
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
    const bookId = $('#submit-button').data('book-id');

    // ⭐ Star click logic
    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            const rating = index + 1;
            ratingInput.value = rating;

            stars.forEach(s => s.classList.remove('fa-star', 'text-warning'));
            stars.forEach(s => s.classList.add('fa-star-o'));

            for (let i = 0; i < rating; i++) {
                stars[i].classList.remove('fa-star-o');
                stars[i].classList.add('fa-star', 'text-warning');
            }
        });
    });

    // ✅ Update sentiment counts
    function updateSentimentCounts(bookId) {
        $.ajax({
            url: `/reviews/sentiment_counts/${bookId}/`,
            method: 'GET',
            success: function (data) {
                $('#count-positive').text(data.positive || 0);
                $('#count-neutral').text(data.neutral || 0);
                $('#count-negative').text(data.negative || 0);

            },
            error: function () {
                console.error("Failed to fetch sentiment counts.");
            }
        });
    }

    updateSentimentCounts(bookId);  // Initial load

    // 📝 AJAX Review Submit
    $('#submit-button').click(function (event) {
        event.preventDefault();

        const rating = $('#rating').val();
        const comment = $('#comment').val().trim();
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
                            <span class="badge bg-info">Sentiment: ${response.review.prediction}</span>
                        </div>
                    </div>
                `;
                $('#review-section').prepend(newReviewHtml);

                // Refresh sentiment counts after successful submit
                $('#sentiment-summary-block').remove();  // Remove previous summary if exists
                updateSentimentCounts(bookId);
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
