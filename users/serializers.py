from rest_framework import serializers
from users.models import User  # Импортируйте кастомную модель
from django.db import IntegrityError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User  # Используйте кастомную модель
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError("Имя пользователя не может быть пустым")
        return value

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data.get('email', ''),
                password=validated_data['password'],
            )
            return user
        except IntegrityError:
            raise serializers.ValidationError({
                "detail": "Пользователь с таким именем или email уже существует"
            })