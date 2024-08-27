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


#decorator in Django is used to restrict access to a view so that only authenticated users can access it.
def Home(request):

    return render(request,'signin/home.html')
#index for master page

def Index(request):

    return render(request,'signin/index.html')

def RegisterView(request):
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
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


# @login_required
def LoginView(request):

    if request.method=='POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)

            return redirect('index')

        else:
            messages.error(request, "Invalid login cradiential")

    return render(request,'signin/login.html')


# Create logout view
#
# def LogoutView(request):
#     logout(request)
#
#     return redirect('login')


# Create Forgot password view
def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            # create a new reset id
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            # create password reset url
            password_reset_url = reverse('reset-password',kwargs={'reset_id': new_password_reset.reset_id})
            full_passwrd_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            # email content
            email_body = f'Reset your password using the link below:\n\n\n{full_passwrd_reset_url}'

            email_messsage = EmailMessage(
                'Reset your password',  # email subject
                email_body,
                settings.EMAIL_HOST_USER,  # email sender
                [email]  # email receiver

            )
            email_messsage.fail_silently = True
            email_messsage.send()

            return redirect('password-reset-sent',reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request,f"No user with email '{email}' found ")
            return redirect('forgot-password')

    return render(request,'signin/forgot_password.html')

# get reset_id make sure that it is valid:
def PasswordResetSent(request,reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request,'signin/password_reset_sent.html')
    else:
         # redirect to forgot password page if code does not exist
        messages.error(request,'Invalid reset id')
        return redirect('forgot-password')


def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)
        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request,'Password do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request,'Password must be at least 5 charecters long')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now()>expiration_time:
                passwords_have_error = True
                messages.error(request,'Reset link has expired')

                reset_id.delete()
                #Reset passsword
            if not passwords_have_error:

                user =password_reset_id.user
                user.set_password(password)
                user.save()
                # delete reset id
                password_reset_id.delete()
                #  redirect to login
                messages.success(request,'password reset.Proceed to login')
                return redirect('login')
            else:
                # redirect to back to password reset page and display errors
                return redirect('reset-password',reset_id=reset_id)


    except PasswordReset.DoesNotExist:

        # redirect to forgot password page if code does not exist
        messages.error(request,'Invalid reset id ')
        return redirect('forgot-password')

    return render(request,'signin/reset_password.html')
