from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.car_list, name='car_list'),
    path('car/<int:pk>/', views.car_details, name='car_details'),
    path('orders/', views.OrderListView.as_view(), name='orderline_list'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='orderline_detail'),
    path('order/my/', views.UserOrderListView.as_view(), name='user_order_list'),
    path('car/my/', views.UserCarListView.as_view(), name='user_car_list'), 
    path('order/form/', views.OrderCreateView.as_view(), name='order_create'),
    path('car/form/', views.CarCreateView.as_view(), name='car_create'),
    path('car/update/<int:pk>/', views.CarUpdateView.as_view(), name='car_update'),
    path('order/cancel/<int:pk>/', views.OrderDeleteView.as_view(), name='order_cancel')
]

