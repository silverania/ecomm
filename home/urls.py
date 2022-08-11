from django.urls import path
from home.views import HomePage
from django.contrib.auth import views
from . import views
app_name = 'shop'
urlpatterns = [
    path('home/', views.HomePage.as_view(), name="HomePage"),
    path('home/products/', views.Product_List.as_view(), name='product_list'),
    path('<slug:category_slug>/', views.Product_List.as_view(),
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/',
         views.Product_Detail.as_view(), name='product_detail'),
]
