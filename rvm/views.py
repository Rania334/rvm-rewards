from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializers import DepositSerializer, UserSerializer
from .utils import calculate_reward
from .models import Deposit

from rest_framework.pagination import PageNumberPagination

class DepositPagination(PageNumberPagination):
    page_size = 10

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deposit_material(request):
    serializer = DepositSerializer(data=request.data)
    if serializer.is_valid():
        deposit = serializer.save(user=request.user)
        points = calculate_reward(deposit.material, deposit.weight)
        return Response({
            'message': 'Deposit successful',
            'weight': deposit.weight,
            'material': deposit.material,
            'machine_id': deposit.machine_id,
            'points_earned': points
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_summary(request):
    deposits = Deposit.objects.filter(user=request.user)
    total_weight = sum(d.weight for d in deposits)
    total_points = sum(calculate_reward(d.material, d.weight) for d in deposits)

    return Response({
        'user': request.user.username,
        'total_weight': total_weight,
        'total_points': total_points,
        'deposit_count': deposits.count()
    })

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_deposits(request):
    deposits = Deposit.objects.filter(user=request.user).order_by('-timestamp')
    paginator = DepositPagination()
    result_page = paginator.paginate_queryset(deposits, request)
    serializer = DepositSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
