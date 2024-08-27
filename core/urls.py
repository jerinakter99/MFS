from django.urls import path
from core import views
# map views to urls
urlpatterns = [
    path('', views.Home, name='home'),
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('index/', views.Index, name='index'),
    # path('logout/',views.LogoutView, name='logout')
    path('forgot-password/',views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent,name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword,name='reset-password'),

]
