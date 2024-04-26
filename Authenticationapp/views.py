from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.generic import View
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import generate_token
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import user_passes_test

import re

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
# views.py

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})


def signup(request):
    context = {'dis': 'inline'}

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email-id')
        passw = request.POST.get('userpass')
        cpassw = request.POST.get('cuserpass')

        if len(passw) <= 8:
            messages.warning(request, "Password is not long enough🙂", context)
            return redirect('/auth/signup/')

        # Add other password validation checks here

        if passw != cpassw:
            messages.warning(request, "Password does not match☹️", context)
            return redirect('/auth/signup/')

        # Generate OTP
        otp = ''.join(random.choices('0123456789', k=6))  # 6-digit OTP

        try:
            if User.objects.get(username=username):
                messages.warning(request, "User already exists☹️", context)
                return redirect('/auth/signup/')
        except User.DoesNotExist:
            pass

        # Store OTP (in session or database)
        request.session['signup_otp'] = otp
        request.session['signup_username'] = username
        request.session['signup_email'] = email
        request.session['signup_passw'] = passw

        # Send OTP via email
        send_activation_email(email, otp)

        messages.info(request, "An OTP has been sent to your email. Please check and verify.", context)

        return render(request, 'Account/verify_otp.html', context)

    return render(request, 'Account/signup.html', context)

def verify_otp(request):
    context = {'dis': 'inline'}

    if request.method == 'POST':
        user_input_otp = request.POST.get('otp')
        stored_otp = request.session.get('signup_otp')

        if user_input_otp == stored_otp:
            # Activate account
            username = request.session.get('signup_username')
            email = request.session.get('signup_email')
            passw = request.session.get('signup_passw')

            user = User.objects.create_user(username, email, passw)
            user.is_active = True
            user.save()

            messages.success(request, "Account activated successfully! You can now login.", context)
            return redirect('/auth/login/')
        else:
            messages.error(request, "Invalid OTP. Please try again.", context)
            return redirect('/auth/verify-otp/')

    return render(request, 'Account/verify_otp.html', context)

def send_activation_email(email, otp):
    subject = 'Your OTP for account verification'
    html_message = render_to_string('Account/activate.html', {'otp': otp})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=html_message)

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activated Successfully")
            return render(request,'../templates/Account/login.html')
        return render(request,'activate.html')

def logins(request):
    context={
                'dis':'inline'
            }
    if request.method=='POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        try:
            username = User.objects.filter(username=name).first()
        except User.DoesNotExist:
            username = None
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            user.is_active=True
            messages.warning(request, "You have successfully logged in as "+name+".", context)
            return redirect('/')
        else:
            messages.warning(request, "Your email "+name+" or password is incorrect", context)
            return render(request,'../templates/Account/login.html')

    return render(request,'Account/login.html')
def logouth(request):
    logout(request)
    return redirect('/')


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def logout_req(request):
    logout(request)
    return redirect('/admin/login/')


# def My_Account(request):
#     # Your view logic here
#     return render(request, 'my_account.html', {})