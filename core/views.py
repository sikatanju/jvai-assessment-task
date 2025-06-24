from django.http.response import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response




from .models import UserProfile
from .serializers import UserProfileSerializer 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hello(request):
    user_serializer = UserProfileSerializer(UserProfile.objects.get(user=request.user))
    return Response({"user_profile": user_serializer.data})





