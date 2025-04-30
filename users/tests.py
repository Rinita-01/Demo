import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
from unittest.mock import patch, ANY

@pytest.fixture
def user_data():
    return {
        'email': 'testuser@example.com',
        'password': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'testuser',
        'dob': '2000-01-01',
        'gender': 'M',
        'phone': '1234567890',
        'address': '123 Test Street',
    }

@pytest.mark.django_db
@patch('users.views.send_verification_email')  # Important: 'users.views' because it's imported there
def test_customer_registration_success(mock_send_email, client, user_data):
    profile_picture = SimpleUploadedFile(
        name='test_image.jpg',
        content=b'\x47\x49\x46\x38\x39\x61',  # Minimal valid GIF file header
        content_type='image/gif'
    )
    data = user_data.copy()
    data['profile_picture'] = profile_picture

    url = reverse('customer_registration')  # Replace if your URL name is different
    response = client.post(url, data)

    assert response.status_code == 200
    assert response.json()['success'] is True

    user = User.objects.get(email='testuser@example.com')
    assert user.is_active is False
    assert user.user_type == 'customer'

    mock_send_email.assert_called_once_with(
        ANY,  # request
        user,
        'Activate your account',
        'users/emails/account_verification_email.html'
    )

@pytest.mark.django_db
def test_customer_login_success(client, django_user_model):
    # Create user manually
    user = django_user_model.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpassword123',
        user_type='customer',
        is_active=True
    )

    url = reverse('customer_login')
    data = {
        'email': 'testuser@example.com',
        'password': 'testpassword123'
    }
    response = client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    assert response.status_code == 200
    json_data = response.json()
    assert json_data['success'] is True
    assert '/users/myAccount/' in json_data['redirect_url']

@pytest.mark.django_db
def test_customer_login_failure_invalid_credentials(client):
    url = reverse('customer_login')
    data = {
        'email': 'wrong@example.com',
        'password': 'wrongpassword'
    }
    response = client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    assert response.status_code == 200
    json_data = response.json()
    assert json_data['success'] is False
    assert json_data['error'] == 'Invalid email or password.'

@pytest.mark.django_db
def test_customer_login_failure_non_customer(client, django_user_model):
    # Create a non-customer user
    user = django_user_model.objects.create_user(
        email='admin@example.com',
        username='adminuser',
        password='adminpassword',
        user_type='admin',
        is_active=True
    )

    url = reverse('customer_login')
    data = {
        'email': 'admin@example.com',
        'password': 'adminpassword'
    }
    response = client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    assert response.status_code == 200
    json_data = response.json()
    assert json_data['success'] is False
    assert json_data['error'] == 'Only customers are allowed to log in.'