from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'username', 'phone', 'address',
            'dob', 'gender', 'email', 'user_type', 'password', 'profile_picture'
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password in responses
            'email': {'required': True},
            'username': {'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)  # Hash the password
        instance.save()
        return instance



# users/serializers.py

from rest_framework import serializers
from .models import User

class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'password', 'first_name', 'last_name', 'username',
            'dob', 'gender', 'phone', 'address', 'profile_picture'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = User(
            **validated_data,
            is_staff=True,
            is_superuser=True,
            user_type='admin'
        )
        user.set_password(password)  # always use set_password
        user.save()
        return user

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)  # Assuming username=email for authentication
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('Account is inactive.')
            if not user.is_staff or not user.is_superuser:
                raise serializers.ValidationError('Not authorized as an admin.')

            data['user'] = user
        else:
            raise serializers.ValidationError('Both email and password are required.')
        
        return data