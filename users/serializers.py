from rest_framework import serializers
from users.models import User  
from django.db import IntegrityError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User  
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError("Имя пользователя не может быть пустым")
        return value

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],  # Set username to the same as the name
                email=validated_data.get('email', ''),
                password=validated_data['password'],
                first_name=validated_data['username'],  # Set first_name to match username
            )
            return user
        except IntegrityError:
            raise serializers.ValidationError({
                "detail": "Пользователь с таким именем или email уже существует"
            })