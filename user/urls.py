from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include

urlpatterns = [
    # path('login/', views.LoginView.as_view(), name='login'),
    path('login/blog', views.user_login, name='login'),
    path('blog/getuser', views.checkUser.as_view(), name='checkuser'),
    re_path('login', views.user_login, name='login'),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('logout/blog', views.Logout.as_view(), name="logout"),
    re_path('register/', views.user_register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    # path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('edit/', views.edit, name='edit'),
    path('social-auth/', include('social_django.urls')),
]
