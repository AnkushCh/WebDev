from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .forms import *

import json
import urllib

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,'index.html')

def login_view(request,backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == 'POST':
        form = BootstrapAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user,backend='django.contrib.auth.backends.ModelBackend')
                messages.info(request, f"You are now logged in as {username}")
                if user.is_superuser or user.is_staff:
                    return redirect('/admin')
                else:
                    return redirect('/dashboard')
    else:
        form = BootstrapAuthenticationForm()
    return render(request = request,template_name = "login.html",context={"form":form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''
            if result['success']:
                email.send()
                msg = 'Please verify your email address to complete the registration. Check your email inbox for verification link'
                messages.success(request, msg)
                return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token,backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
            # return redirect('home')
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('Activation link is invalid!')