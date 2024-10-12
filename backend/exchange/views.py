from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .models import Exchange
from .serializers import ExchangeSerializer

# Create your views here.
EXCHANGE_API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&data=AP01'

# 환율 정보 조회 및 업데이트
@api_view(['GET'])
def index(request):
    response = requests.get(EXCHANGE_API_URL).json()
    existing_exchanges = Exchange.objects.all()
    if response:
        if not existing_exchanges:
            serializer = ExchangeSerializer(data=response, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            existing_exchanges.delete()
            serializer = ExchangeSerializer(data=response, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
    serializer = ExchangeSerializer(existing_exchanges, many=True)
    return Response(serializer.data)
