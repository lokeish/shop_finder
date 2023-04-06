from django.urls import path
from . import views

urlpatterns = [
    path('create_shop/', views.create_shop, name='create_shop'),
    path('update_shop/<int:pk>/', views.update_shop, name='update_shop'),
    path('shop_detail/<int:pk>/',views.shop_detail, name='shop_detail'),
    path('shop_search', views.search_shops, name='shop_search'),
    path('', views.shop_list, name='shop_list'),
]