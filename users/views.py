from django.shortcuts import render, redirect
from django.http import JsonResponse
from users.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from .decoraters import custom_login_required
from orders.models import Order
import logging


logger = logging.getLogger(__name__)


@custom_login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders}) 
    
# @login_required(login_url='customer_login')
def myAccount(request):
    return render(request, 'users/my_account.html', {
        'user': request.user,
    })


def activate(request, uidb64, token):              
    try:
        # Decode user ID from the URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if the user exists and the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Activate user
        user.save()
        messages.success(request, 'Congratulations! Your account has been activated.')
        return redirect('customer_login')  # Redirect to login page
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('customer_login')  # Redirect to login page if activation fails


def send_verification_email(request, user, mail_subject, email_template):
    """Function to send an email verification link"""
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
    email.content_subtype = "html"
    email.send()


def admin_registration(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            profile_picture = request.FILES.get('profile_picture')

            # Debugging log to check the received data
            logger.debug(f"Received Data: {email}, {username}, {first_name}, {last_name}")

            # Ensure the data is valid
            if not email or not password or not username:
                return JsonResponse({'success': False, 'error': 'Missing required fields.'})

            # Create the User instance
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                gender=gender,
                phone=phone,
                address=address,
                profile_picture=profile_picture
            )

            # Set the user as admin
            user.is_staff = True  # Grant admin rights
            user.is_superuser = True  # Grant superuser rights
            user.user_type = 'admin'  # Optional if using a user_type field
            user.save()

            # Log in the user immediately after registration
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)

            # Return success response with redirect URL for the admin panel login
            return JsonResponse({
                'success': True, 
                'message': 'Registration successful!', 
                'redirect_url': '/admin/login/'
            })

        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})

    gender_choices = User._meta.get_field('gender').choices 
    return render(request, 'users/admin_registration.html', {'gender_choices': gender_choices})


def customer_registration(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            profile_picture = request.FILES.get('profile_picture')  

            print(email, password, first_name, last_name, username, dob, gender, phone, address, profile_picture)

            # Create User instance with inactive status
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                username=username,
                dob=dob,
                gender=gender,
                phone=phone,
                address=address,
                profile_picture=profile_picture,
            )
            user.is_active = False  # User must verify email before activation
            user.user_type = 'customer'  # Ensure user_type is set to customer
            user.save()

            # Send verification email
            mail_subject = 'Activate your account'
            email_template = 'users/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            return JsonResponse({'success': True, 'message': 'Registration successful!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
    gender_choices = User._meta.get_field('gender').choices
    return render(request, 'users/customer_registration.html', {'gender_choices': gender_choices})


def customer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Check if the user is a customer
            if user.user_type == 'customer':  # Ensure that the user is a customer
                login(request, user)
                
                # Check if the request is AJAX
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({"success": True, "redirect_url": "/users/myAccount/"})
                else:
                    return redirect('myAccount')
            else:
                # If the user is not a customer, show an error message
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({"success": False, "error": "Only customers are allowed to log in."})
                else:
                    messages.error(request, "Only customers are allowed to log in.")
                    return redirect('customer_login')

        else:
            # If authentication fails
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "error": "Invalid email or password."})
            else:
                messages.error(request, "Invalid email or password")
                return redirect('customer_login')

    return render(request, 'users/customer_login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('home')
    add_never_cache_headers(response)
    return response



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.contrib.auth import authenticate, login
from .models import User  # import your User model
import logging
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from .serializers import AdminLoginSerializer


logger = logging.getLogger(__name__)

# Admin Registration through Class Based View
@method_decorator(csrf_exempt, name='dispatch')
class AdminRegistrationAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Handles form-data + file uploads

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            username = request.data.get('username')
            dob = request.data.get('dob')
            gender = request.data.get('gender')
            phone = request.data.get('phone')
            address = request.data.get('address')
            profile_picture = request.FILES.get('profile_picture')

            logger.debug(f"Received Data: {email}, {username}, {first_name}, {last_name}")

            # Validate required fields
            if not email or not password or not username:
                return Response({'success': False, 'error': 'Missing required fields (email, username, or password).'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the admin user
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                username=username,
                dob=dob,
                gender=gender,
                phone=phone,
                address=address,
                profile_picture=profile_picture
            )
            user.is_staff = True
            user.is_superuser = True
            user.user_type = 'admin'
            user.save()

            # Login the user immediately
            authenticated_user = authenticate(request, email=email, password=password)
            if authenticated_user:
                login(request, authenticated_user)

            return Response({
                'success': True,
                'message': 'Admin registration successful!',
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error during admin registration: {str(e)}")
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Admin Login through Class Based View
class AdminLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            return Response({
                'success': True,
                'message': 'Admin login successful!',
            }, status=status.HTTP_200_OK)
        
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
