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


# account create

def account(request):
    user=request.user
    account, created = Accounts.objects.get_or_create(user=user)
    # import pdb; pdb.set_trace()
    context= {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'name': account.name,
        'type': account.type,
        'pic': account.pic,
        'phone': account.phone,
        'dob': account.dob,
        'gender': account.gender,
        'city': account.city,
        # 'street': account.street,
        'state': account.state,
        'postal_code': account.postal_code,
        'country': account.country,
        'created_at': account.created_at,
        'updated_at': account.updated_at,
        # 'created_by': account.created_by,
        # 'updated_by': account.updated_by

    }
    return render(request,'accounts/account.html',context)

@login_required
def edit_account(request):
    user = request.user
    account = user.useraccount

# retrieves or obtains the value
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        name = request.POST.get('name')
        type = request.POST.get('type')
        pic = request.POST.get('pic')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        created_at =request.POST.get('created_at')
        created_by = request.POST.get('created_by')
        updated_at =request.POST.get('updated_at')
        updated_by = request.POST.get('updated_by')


 #  handles the updating of user and account profile information
        # Handle file upload
        if 'pic' in request.FILES:
           account.pic = request.FILES['pic']
        # import pdb ; pdb.set_trace()
        # Update user and profile details
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()

        account.name = name
        account.type = type
        # account.pic = pic
        account.phone = phone
        account.dob = dob
        account.gender = gender
        account.city = city
        account.state = state
        account.postal_code = postal_code

        # account.created_by = created_by
        # account.updated_by = updated_by
        account.save()

        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('account')
# creates a dictionary named context that holds the data to be passed to the template for rendering the html page.
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'name': account.name,
        'type': account.type,
        'pic': account.pic,
        'phone': account.phone,
        'dob': account.dob,
        'gender': account.gender,
        'city': account.city,
        # 'street': account.street,
        'state': account.state,
        'postal_code': account.postal_code,
        'country': account.country,

    }

    return render(request, 'accounts/edit.html', context)