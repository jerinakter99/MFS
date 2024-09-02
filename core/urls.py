from django.urls import path
from core import views
from django.conf.urls.static import static
from django.conf import settings
# map views to urls
urlpatterns = [
    path('', views.Home, name='home'),
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('index/', views.Index, name='index'),
    # path('logout/',views.LogoutView, name='logout')
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent,name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword,name='reset-password'),
    path('account/', views.account,name='account'),
    path('account_edit/', views.edit_account, name='account_edit'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)