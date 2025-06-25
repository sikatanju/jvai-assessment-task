from django.http.response import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import UserProfile, User
from .serializers import UserProfileSerializer, UserRegisterSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user_serializer = UserProfileSerializer(UserProfile.objects.get(user=request.user))
    return Response({"user_profile": user_serializer.data})


@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        user_serializer = UserRegisterSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()  
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def user_activate(request):
    email = request.GET.get('email')
    if email:
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                user.is_active = True
                user.save()

        except User.DoesNotExist():
            return Response({"message": "Wrong activation link"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Account activated successfully"})


