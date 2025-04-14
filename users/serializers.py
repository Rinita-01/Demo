from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'username', 'phone', 'address',
            'dob', 'gender', 'email', 'user_type', 'password'
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
