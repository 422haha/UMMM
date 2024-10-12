from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer, UserInfoSerializer

# Create your views here.
User = get_user_model()

# 사용자 프로필 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, username):
    if request.user.username == username:
        user = get_object_or_404(User, username=username)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

# 사용자 정보 조회 및 수정
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_info(request, username):
    if request.user.username == username:
        user = get_object_or_404(User, username=username)
        if request.method == 'GET':
            serializer = UserInfoSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserInfoSerializer(instance=user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

# 사용자 프로필 이미지 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_info_profile(request, username):
    if request.user.username == username:
        user = get_object_or_404(User, username=username)
        data = {'profile_img': request.data.get('profile_img[]')}
        serializer = UserInfoSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
