from django.urls import path
from . import views


urlpatterns = [
    path('save_financial_products/', views.save_financial_products),
    path('deposit_list/', views.deposit_list),
    path('saving_list/', views.saving_list),
    path('deposit_list/<str:deposit_code>/', views.get_deposit_detail),
    path('saving_list/<str:saving_code>/', views.get_saving_detail),
    path('deposit_list/<str:deposit_code>/contract/', views.contract_deposit),
    path('saving_list/<str:saving_code>/contract/', views.contract_saving),
    path('recommend/', views.recommend_products),
    path('recommend_chart/', views.recommend_chart),
    path('highest_deposit/', views.highest_deposit),
    path('highest_saving/', views.highest_saving),
    path('highest_rate_product/', views.highest_rate_product),
]