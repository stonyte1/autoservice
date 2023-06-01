from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.car_list, name='car_list'),
    path('car/<int:pk>/', views.car_details, name='car_details'),
    path('orders/', views.OrderListView.as_view(), name='orderline_list'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='orderline_detail')
]
