from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

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
            user = user_serializer.save(is_active=False)
            user.save()
            return Response({"message": "User successfully created, check your email (console) to activate your account."}, status=status.HTTP_201_CREATED)
        
        return Response({"message": "error occurred, try again later"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def user_activate(request):
    email = request.GET.get('email')
    token = request.GET.get('token')
    if email and token:
        try:
            user = User.objects.get(email=email)
            try:
                token_old = Token.objects.filter(user=user).values('key').first()
            except Token.DoesNotExist():
                return Response({"message": "Wrong activation link"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not user.is_active and token == token_old['key']:
                user.is_active = True
                user.save()
                return Response({"message": "Account activated successfully."}, status=status.HTTP_202_ACCEPTED)
            elif user.is_active:
                return Response({"message": "Account already activated."}, status=status.HTTP_200_OK)
            
        except User.DoesNotExist():
            return Response({"message": "Wrong activation link"}, status=status.HTTP_400_BAD_REQUEST)
        
        
    return Response({"error": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)


