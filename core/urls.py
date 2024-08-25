from django.urls import path
from core import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('index/', views.Index, name='index'),

]
