from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from rest_framework.exceptions import ValidationError
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=128, write_only=True)
    re_password = serializers.CharField(min_length=8, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 're_password', 'email']

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        if not self.instance or 'password' in attrs or 're_password' in attrs:
            if attrs.get('password') != attrs.get('re_password'):
                raise serializers.ValidationError({'re_password': 'Passwords do not match!!'})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('re_password')
        return User.objects.create_user(**validated_data)