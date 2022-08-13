from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'shop'

urlpatterns = [
    path('home/', views.Product_List.as_view(), name="home"),
    path('home/products/', views.Product_List.as_view(), name='product_list'),
    path('<slug:category_slug>/', views.Product_List.as_view(),
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/',
         views.Product_Detail.as_view(), name='product_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
