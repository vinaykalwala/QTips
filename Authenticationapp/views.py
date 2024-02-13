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
def signup(request):
    context={
        'dis':'inline'
    }
    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email-id')
        passw = request.POST.get('userpass')
        cpassw = request.POST.get('cuserpass')
        if len(passw)<=8:
            messages.warning(request,"Password is not long enough🙂",context)
            return redirect('/auth/signup/')
        if not re.search("[a-z]", passw) :
            messages.warning(request,"Password should contain atleast a lowercase🙂",context)
            return redirect('/auth/signup/')
        if not re.search("[A-Z]", passw) :
            messages.warning(request,"Password should contain atleast an uppercase🙂",context)
            return redirect('/auth/signup/')
        if not re.search("[0-9]", passw) :
            messages.warning(request,"Password should contain atleast a numerical🙂",context)
            return redirect('/auth/signup/')
        if not re.search("[_@$]" , passw) :
            messages.warning(request,"Password should contain atleast a special character🙂",context)
            return redirect('/auth/signup/')
        if re.search("\s" , passw) :
            messages.warning(request,"Password should not contain spaces🙂",context)
            return redirect('/auth/signup/')
        if passw!=cpassw :
            messages.warning(request,"Password is not match☹️",context)
            return redirect('/auth/signup/')
        try:
            if User.objects.get(username=username):
                    messages.warning(request,"User is already there☹️",context)
                    # return render(request,'Authentication/signup.html')
                    return redirect('/auth/signup/')

        except:
            pass

        user= User.objects.create_user(username,email,passw)
        user.is_active=False
        user.save()
        email_subject='Activate your account'
        message=get_template('../templates/Account/Activate_acc.html').render({
            'user':user.email,
            'domain':'https://www.qtipstore.com',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user),
        })

        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [user.email])
        email_message.content_subtype='html'
        email_message.send()
        #           )
        messages.warning(request, "Please check your inbox for a verification link, as it has been sent to you for authentication purposes. Thank you.", context)

        return render(request,'Account/login.html')

    return render(request,'../templates/Account/signup.html')

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