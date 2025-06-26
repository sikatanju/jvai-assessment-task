from rest_framework import serializers

from .models import UserProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model= UserProfile
        fields = ['id', 'user', 'phone', 'birth_date', 'profile_pic']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        
        extra_kwargs = {'password': {'write_only': True}, 'first_name': {'required': False}, 'last_name': {'required': False}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)