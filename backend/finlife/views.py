import random
import requests
import pandas as pd
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import User
from .models import Deposit, Saving, DepositOption, SavingOption
from .serializers import (
    DepositSerializer, SavingSerializer, 
    DepositOptionSerializer, SavingOptionSerializer, 
    ContractDepositSerializer, ContractSavingSerializer
)
from sklearn.neighbors import NearestNeighbors

# 외부 API에서 금융 상품 데이터를 가져와 데이터베이스에 저장하는 함수
API_KEY = settings.FINLIFE_API_KEY

@api_view(['GET'])
def save_financial_products(request):
    """외부 API에서 금융 상품(예금 및 적금) 데이터를 가져와 저장"""

    # 예금 및 적금 상품에 대한 API URL
    DEPOSIT_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    SAVING_API_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    # 예금 데이터 가져오기
    deposit_res = requests.get(DEPOSIT_API_URL).json()
    deposit_baseList = deposit_res.get('result').get('baseList')
    deposit_optionList = deposit_res.get('result').get('optionList')

    # 예금 데이터를 데이터베이스에 저장
    for base in deposit_baseList:
        if Deposit.objects.filter(deposit_code=base.get('fin_prdt_cd')).exists():
            continue
        save_product = {
            'deposit_code': base.get('fin_prdt_cd', '-1'),   # 예금 코드 설정
            'kor_co_nm': base.get('kor_co_nm', '-1'),        # 회사명 설정
            'fin_prdt_nm': base.get('fin_prdt_nm', '-1'),    # 상품명 설정
            'mtrt_int': base.get('mtrt_int', '-1'),          # 만기 이자 설정
            'etc_note': base.get('etc_note', '-1'),          # 기타 노트 설정
            'join_deny': base.get('join_deny', -1),          # 가입 불가 여부 설정
            'join_member': base.get('join_member', '-1'),    # 가입 대상 설정
            'join_way': base.get('join_way', '-1'),          # 가입 방법 설정
            'spcl_cnd': base.get('spcl_cnd', '-1'),          # 특수 조건 설정
            'max_limit': base.get('max_limit', -1),          # 최대 한도 설정
        }
        serializer = DepositSerializer(data=save_product)   # 예금 데이터 직렬화
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # 데이터가 유효하면 저장

    # 예금 옵션 데이터를 데이터베이스에 저장
    for option in deposit_optionList:
        prdt_cd = option.get('fin_prdt_cd', '-1')  # 상품 코드 가져오기
        product = get_object_or_404(Deposit, deposit_code=prdt_cd)  # 예금 객체 가져오기
        save_option = {
            'intr_rate_type_nm': option.get('intr_rate_type_nm', '-1'),  # 이자율 유형 이름 설정
            'intr_rate': option.get('intr_rate', -1),                    # 이자율 설정
            'intr_rate2': option.get('intr_rate2', -1),                  # 추가 이자율 설정
            'save_trm': option.get('save_trm', -1),                      # 저축 기간 설정
        }
        serializer = DepositOptionSerializer(data=save_option)  # 예금 옵션 데이터 직렬화
        if serializer.is_valid(raise_exception=True):
            serializer.save(deposit=product)  # 데이터가 유효하면 저장

    # 적금 데이터 가져오기
    saving_res = requests.get(SAVING_API_URL).json()
    saving_baseList = saving_res.get('result').get('baseList')
    saving_optionList = saving_res.get('result').get('optionList')

    # 적금 데이터를 데이터베이스에 저장
    for base in saving_baseList:
        if Saving.objects.filter(saving_code=base.get('fin_prdt_cd')).exists():
            continue
        save_product = {
            'saving_code': base.get('fin_prdt_cd', '-1'),    # 적금 코드 설정
            'kor_co_nm': base.get('kor_co_nm', '-1'),        # 회사명 설정
            'fin_prdt_nm': base.get('fin_prdt_nm', '-1'),    # 상품명 설정
            'mtrt_int': base.get('mtrt_int', '-1'),          # 만기 이자 설정
            'etc_note': base.get('etc_note', '-1'),          # 기타 노트 설정
            'join_deny': base.get('join_deny', -1),          # 가입 불가 여부 설정
            'join_member': base.get('join_member', '-1'),    # 가입 대상 설정
            'join_way': base.get('join_way', '-1'),          # 가입 방법 설정
            'spcl_cnd': base.get('spcl_cnd', '-1'),          # 특수 조건 설정
            'max_limit': base.get('max_limit', -1),          # 최대 한도 설정
        }
        serializer = SavingSerializer(data=save_product)  # 적금 데이터 직렬화
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # 데이터가 유효하면 저장

    # 적금 옵션 데이터를 데이터베이스에 저장
    for option in saving_optionList:
        prdt_cd = option.get('fin_prdt_cd', '-1')  # 상품 코드 가져오기
        product = get_object_or_404(Saving, saving_code=prdt_cd)  # 적금 객체 가져오기
        save_option = {
            'intr_rate_type_nm': option.get('intr_rate_type_nm', '-1'),  # 이자율 유형 이름 설정
            'rsrv_type_nm': option.get('rsrv_type_nm', '-1'),            # 적립 유형 이름 설정
            'intr_rate': option.get('intr_rate', -1),                    # 이자율 설정
            'intr_rate2': option.get('intr_rate2', -1),                  # 추가 이자율 설정
            'save_trm': option.get('save_trm', -1),                      # 저축 기간 설정
        }
        serializer = SavingOptionSerializer(data=save_option)  # 적금 옵션 데이터 직렬화
        if serializer.is_valid(raise_exception=True):
            serializer.save(saving=product)  # 데이터가 유효하면 저장

    return Response({"message": "Financial products saved successfully."})  # 성공 메시지 반환

# 예금 데이터를 불러오는 함수
@api_view(['GET'])
def deposit_list(request):
    deposits = Deposit.objects.all()
    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)

# 적금 데이터를 불러오는 함수
@api_view(['GET'])
def saving_list(request):
    savings = Saving.objects.all()
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)

# 예금 디테일 데이터를 불러오는 함수
@api_view(['GET'])
def get_deposit_detail(request, deposit_code):
    deposit = get_object_or_404(Deposit, deposit_code=deposit_code)
    deposit_options = DepositOption.objects.filter(deposit=deposit)

    deposit_data = {
        'kor_co_nm': deposit.kor_co_nm,
        'fin_prdt_nm': deposit.fin_prdt_nm,
        'join_way': deposit.join_way,
        'mtrt_int': deposit.mtrt_int,
        'spcl_cnd': deposit.spcl_cnd,
        'join_deny': deposit.join_deny,
        'join_member': deposit.join_member,
        'etc_note': deposit.etc_note,
        'max_limit': deposit.max_limit,
        'options': [{
            'save_trm': option.save_trm,
            'intr_rate': option.intr_rate,
            'intr_rate2': option.intr_rate2,
        } for option in deposit_options]
    }

    return JsonResponse(deposit_data)

# 적금 디테일 데이터를 불러오는 함수
@api_view(['GET'])
def get_saving_detail(request, saving_code):
    saving = get_object_or_404(Saving, saving_code=saving_code)
    saving_options = SavingOption.objects.filter(saving=saving)

    saving_data = {
        'kor_co_nm': saving.kor_co_nm,
        'fin_prdt_nm': saving.fin_prdt_nm,
        'join_way': saving.join_way,
        'mtrt_int': saving.mtrt_int,
        'spcl_cnd': saving.spcl_cnd,
        'join_deny': saving.join_deny,
        'join_member': saving.join_member,
        'etc_note': saving.etc_note,
        'max_limit': saving.max_limit,
        'options': [{
            'rsrv_type_nm': option.rsrv_type_nm,
            'save_trm': option.save_trm,
            'intr_rate': option.intr_rate,
            'intr_rate2': option.intr_rate2,
        } for option in saving_options]
    }

    return JsonResponse(saving_data)

# 사용자가 예금 상품과 계약을 맺는 함수
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def contract_deposit(request, deposit_code):
    deposit = get_object_or_404(Deposit, deposit_code=deposit_code)
    
    if request.method == 'GET':
        serializer = ContractDepositSerializer(deposit)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if request.user in deposit.contract_user.all():
            deposit.contract_user.remove(request.user)
            
            # financial_products에서 deposit_code 제거
            financial_products = request.user.financial_products.split(',') if request.user.financial_products else []
            if deposit_code in financial_products:
                financial_products.remove(deposit_code)
                request.user.financial_products = ','.join(financial_products)
                request.user.save()
            
            return Response({"detail": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "삭제할 항목이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        if request.user not in deposit.contract_user.all():
            deposit.contract_user.add(request.user)
            
            # financial_products에 deposit_code 추가
            financial_products = request.user.financial_products.split(',') if request.user.financial_products else []
            if deposit_code not in financial_products:
                financial_products.append(deposit_code)
                request.user.financial_products = ','.join(financial_products)
                request.user.save()

            serializer = ContractDepositSerializer(deposit, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"detail": "상품이 추가되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "이미 상품이 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)

# 사용자가 적금 상품과 계약을 맺는 함수
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def contract_saving(request, saving_code):
    saving = get_object_or_404(Saving, saving_code=saving_code)
    
    if request.method == 'GET':
        serializer = ContractSavingSerializer(saving)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if request.user in saving.contract_user.all():
            saving.contract_user.remove(request.user)
            
            # financial_products에서 saving_code 제거
            financial_products = request.user.financial_products.split(',') if request.user.financial_products else []
            if saving_code in financial_products:
                financial_products.remove(saving_code)
                request.user.financial_products = ','.join(financial_products)
                request.user.save()
            
            return Response({"detail": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "삭제할 항목이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        if request.user not in saving.contract_user.all():
            saving.contract_user.add(request.user)
            
            # financial_products에 saving_code 추가
            financial_products = request.user.financial_products.split(',') if request.user.financial_products else []
            if saving_code not in financial_products:
                financial_products.append(saving_code)
                request.user.financial_products = ','.join(financial_products)
                request.user.save()

            serializer = ContractSavingSerializer(saving, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"detail": "상품이 추가되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "이미 상품이 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)

# 사용자에게 금융 상품 추천하는 함수
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_products(request):
    # 데이터베이스에서 사용자 데이터 가져오기
    User = get_user_model()
    users = User.objects.all().values('id', 'age', 'property', 'annual_salary', 'financial_products')

    # 사용자 데이터에서 DataFrame 만들기
    df_users = pd.DataFrame(users)

    # feature 열 추출
    feature_cols = ['age', 'property', 'annual_salary']

    # financial_products를 제품 목록으로 변환
    df_users['financial_products'] = df_users['financial_products'].apply(lambda x: x.split(',') if x else [])

    X = df_users[feature_cols].fillna(0).values

    # K-최근접 이웃 알고리즘(K-Nearest Neighbor)을 사용하여 추천 (Train a k-NN model)
    knn = NearestNeighbors(n_neighbors=10, algorithm='auto')
    knn.fit(X)

    def recommend_products(user_id, n_recommendations=5):
        # 대상 사용자 찾기
        target_user = df_users[df_users['id'] == user_id]

        if target_user.empty:
            return []

        # 대상 사용자의 features 추출
        target_user_features = target_user[feature_cols].fillna(0).values

        # 가장 가까운 이웃들 찾기
        distances, indices = knn.kneighbors(target_user_features, n_neighbors=10)

        # 가장 가까운 이웃들이 선택한 금융 상품 얻기
        neighbor_ids = indices.flatten()
        neighbor_products = df_users.loc[neighbor_ids, 'financial_products']
        
        # 상품의 빈도수를 count
        all_products = [product for sublist in neighbor_products for product in sublist]
        product_counts = pd.Series(all_products).value_counts()

        # 가장 많이 가입한 상위 n개 상품 추천
        recommended_products = product_counts.head(n_recommendations).index.tolist()
        return recommended_products

    user = request.user
    user_id = user.id if user.is_authenticated else 1  # 사용자가 인증되지 않은 경우 기본 사용
    recommended_products = recommend_products(user_id)

    # 데이터베이스에서 추천 상품 가져오기
    recommended_deposits = Deposit.objects.filter(deposit_code__in=recommended_products)
    recommended_savings = Saving.objects.filter(saving_code__in=recommended_products)

    # 추천 상품 Serialize
    deposit_serializer = DepositSerializer(recommended_deposits, many=True)
    saving_serializer = SavingSerializer(recommended_savings, many=True)

    return Response({
        'recommended_deposits': deposit_serializer.data,
        'recommended_savings': saving_serializer.data
    })

# 사용자에게 금융 상품 추천하는 함수
@api_view(['GET'])
def recommend_chart(request):
    top_deposit_options = DepositOption.objects.order_by('-intr_rate2')[:10]
    top_saving_options = SavingOption.objects.order_by('-intr_rate2')[:10]

    top_deposits = Deposit.objects.filter(deposit_code__in=[option.deposit.deposit_code for option in top_deposit_options])
    top_savings = Saving.objects.filter(saving_code__in=[option.saving.saving_code for option in top_saving_options])

    all_deposits = list(Deposit.objects.all())
    all_savings = list(Saving.objects.all())

    # 예금과 적금 데이터를 각각 직렬화
    top_deposit_serializer = DepositSerializer(top_deposits, many=True)
    top_saving_serializer = SavingSerializer(top_savings, many=True)
    
    random_deposits = random.sample(all_deposits, min(len(all_deposits), 5))
    random_savings = random.sample(all_savings, min(len(all_savings), 5))

    random_deposit_serializer = DepositSerializer(random_deposits, many=True)
    random_saving_serializer = SavingSerializer(random_savings, many=True)
    
    # 직렬화된 데이터를 합침
    combined_random_products = random_deposit_serializer.data + random_saving_serializer.data
    # 합친 데이터에서 랜덤으로 5개를 선택
    random_products = random.sample(combined_random_products, min(len(combined_random_products), 5))

    return Response({
        'top_deposits': top_deposit_serializer.data,
        'top_savings': top_saving_serializer.data,
        'random_products': random_products,
    })

# 가장 높은 이자율의 예금 상품을 반환하는 함수
@api_view(['GET'])
def highest_deposit(request):
    """가장 높은 이자율의 예금 상품을 반환"""

    highest_rate_deposit = DepositOption.objects.order_by('-intr_rate2').first()
    if highest_rate_deposit:
        deposit = highest_rate_deposit.deposit
        serializer = DepositSerializer(deposit)
        return Response(serializer.data)
    return Response({"error": "No deposits found."})  # 예금 상품이 없을 경우 오류 반환

# 가장 높은 이자율의 적금 상품을 반환하는 함수
@api_view(['GET'])
def highest_saving(request):
    """가장 높은 이자율의 적금 상품을 반환"""

    highest_rate_saving = SavingOption.objects.order_by('-intr_rate2').first()
    if highest_rate_saving:
        saving = highest_rate_saving.saving
        serializer = SavingSerializer(saving)
        return Response(serializer.data)
    return Response({"error": "No savings found."})  # 적금 상품이 없을 경우 오류 반환

# 가장 높은 이자율의 금융 상품(예금 또는 적금)을 반환하는 함수
@api_view(['GET'])
def highest_rate_product(request):
    """가장 높은 이자율의 금융 상품(예금 또는 적금)을 반환"""

    highest_deposit = DepositOption.objects.order_by('-intr_rate2').first()
    highest_saving = SavingOption.objects.order_by('-intr_rate2').first()

    if highest_deposit and highest_saving:
        if highest_deposit.intr_rate2 > highest_saving.intr_rate2:
            product = highest_deposit.deposit
            serializer = DepositSerializer(product)
        else:
            product = highest_saving.saving
            serializer = SavingSerializer(product)
        return Response(serializer.data)

    if highest_deposit:
        product = highest_deposit.deposit
        serializer = DepositSerializer(product)
        return Response(serializer.data)

    if highest_saving:
        product = highest_saving.saving
        serializer = SavingSerializer(product)
        return Response(serializer.data)

    return Response({"error": "No financial products found."})  # 금융 상품이 없을 경우 오류 반환
