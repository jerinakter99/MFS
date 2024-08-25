from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages      # for get error massages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from.models import *

# Create your views here.
@login_required
def Home(request):

    return render(request,'signin/home.html')
#index for master page
def Index(request):

    return render(request,'signin/index.html')

def RegisterView(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False
        # validation message
        if User.objects.filter(username=username).exists():
            user_data_has_error=True
            messages.error(request,'Username already exists')

        if User.objects.filter(email=email).exists():
            user_data_has_error=True
            messages.error(request,'Email already exists')

        # validate password length
        if len(password)<5:
            user_data_has_error=True
            messages.error(request,'Password must be at least 5 charecters')
        # if there is error then redirect to the register page
        if user_data_has_error:
            return redirect('register')
        # create new user if there are no errors and redirect to the login page
        else:
            new_user=User.objects.create_user(
                first_name=first_name,
                last_name = last_name,
                email=email,
                username=username,
                password=password
            )
            messages.success(request,'Account created.Login now')
            return redirect('login')


    return render(request,'signin/register.html')

def LoginView(request):
    if request.method=='POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)

            return redirect('index')

        else:
            messages.error(request,"Invalid login cradiential")

    return render(request,'signin/login.html')


# logoutview
# def LogoutView(request):
#     logout(request)
#
#     return redirect('login')
