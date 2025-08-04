from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Deposit

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username must more then 3 characters")
        return value
    def validate_email(self, value):
        if "@" not in value:
            raise serializers.ValidationError("Enter a valid email")
        return value
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password) 
        user.save()
        return user

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['id', 'weight', 'material', 'machine_id', 'timestamp']
