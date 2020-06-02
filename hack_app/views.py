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
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import *
import json
import urllib

from django.conf import settings
from .models import *
from django.views.generic import CreateView,ListView,DetailView,RedirectView
import datetime
# new--------------------------
from formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail
import logging
logr=logging.getLogger(__name__)
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.




def home(request):
    return render(request,'index.html')

def login_view(request):
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
                elif user.groups.filter(name="Organizer").exists():
                    return redirect('org_dashboard')
                else:
                    return redirect('/dashboard')
    else:
        form = BootstrapAuthenticationForm()
    return render(request = request,template_name = "registration/login.html",context={"form":form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
             #   ''' Begin reCAPTCHA validation '''
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
            if result['success']:

                # ''' End reCAPTCHA validation '''
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
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            # return redirect('home')
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('Activation link is invalid!')

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # send email code goes here
            sender = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            mail_subject = name +':'+sender
            message = form.cleaned_data.get('message')
            email = EmailMessage(
                            mail_subject, message, to=["gauravgahlyan999@gmail.com"]
                )
            
            email.send()
            msg = 'Thanks for contacting us. We will respond to you as soon as possible'
            messages.success(request, msg)
            return HttpResponseRedirect('/')
            return HttpResponse('Thanks for contacting us!')
    else:
        form = ContactForm()

    return render(request, 'contact_form.html', {'form': form})

@login_required(login_url='/login/')
def dashboard(request):
    return render(request,'dashboard.html')

@login_required(login_url='/login/')
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'registration/profile.html', args)

@login_required(login_url='/login/')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            phone=request.POST.get('phone')
            Profile.objects.filter(user__username=request.user.username).update(phone_number=phone)
            messages.success(request, "Profile Saved")
            return redirect(reverse('profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'registration/edit_profile.html', args)

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))
        else:
            return redirect(reverse('password_change_form'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'registration/password_change_form.html', args)


# travel reimbersement create view
# @login_required(login_url='/login/')
class TReimburseCreateView(CreateView):
    model=TravelReimbursement
    form_class=TravelReimbursementForm
    template_name="TReimburse.html"
    
    def form_valid(self,form):
        self.object = form.save(commit=False)
        if self.object.user.is_authenticated:
            user=User.objects.get(username=self.request.user.username)
            self.object.user = user
        
            if self.object.travel_date is None:
                self.object.travel_date=datetime.date.today()

            if 'upload_bill' in self.request.FILES:
                self.object.upload_bill=self.request.FILES['upload_bill']
        return super().form_valid(form)    


def group_required(*group_names):
   """Requires user membership in at least one of the groups passed in."""

   def in_groups(u):
       if u.is_authenticated:
           if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
               return True
       return False
   return user_passes_test(in_groups)


# The way to use this decorator is:
# @group_required('Organization',)
def org_dashboard(request):
    return render(request,'org_dashboard.html')


class RegViewWizard( SessionWizardView ):
    instance = None
    template_name="regwizard_form.html" 
    def get_form_instance( self, step ):
        if self.instance is None:
            self.instance = RegModel()
        return self.instance

    def done( self, form_list, **kwargs ):
        user1=User.objects.get(username=self.request.user.username)
        self.instance.user=user1
        self.instance.save()  
        return render(self.request,'dashboard.html')         


class RegsListView(LoginRequiredMixin,ListView):
    login_url='login'
    model=RegModel
    template_name="reglist.html"
    context_object_name="reg_list"  

class RegDetailView(LoginRequiredMixin,DetailView):
    login_url='login'
    model=RegModel
    template_name="regdetail.html" 
    context_object_name="regdetail"


class TravelListView(LoginRequiredMixin,ListView):
    login_url='login'
    model=TravelReimbursement
    template_name="travellist.html"
    context_object_name="travel_list"    

class TravelDetailView(LoginRequiredMixin,DetailView):
    login_url='login'
    model=TravelReimbursement
    template_name="traveldetail.html" 
    context_object_name="traveldetail"

class AcceptTravel(LoginRequiredMixin,RedirectView):
    login_url='login'
    def get_redirect_url(self,*args,**kwargs):
        return reverse('travellists')
    def get(self,request,*args,**kwargs):
        traveluser=TravelReimbursement.objects.filter(id=self.kwargs.get('pk'))
        traveluser.update(accept=True)


        return super().get(request,*args,**kwargs)

class Upvote(LoginRequiredMixin,RedirectView):
    login_url='login'
    def get_redirect_url(self,*args,**kwargs):
        return reverse('reglists')
    def get(self,request,*args,**kwargs):
        reguser=RegModel.objects.get(id=self.kwargs.get('pk'))
        
        try:
            Vote.objects.create(organizer=self.request.user,voteregs_id=reguser.id)
        except IntegrityError:
            print('already voted')
        else:
            reguser.votes_total=reguser.votes_total+1
            reguser.save()
            


        return super().get(request,*args,**kwargs)

class Downvote(LoginRequiredMixin,RedirectView):
    login_url='login'
    def get_redirect_url(self,*args,**kwargs):
        return reverse('reglists')
    def get(self,request,*args,**kwargs):
        reguser=RegModel.objects.get(id=self.kwargs.get('pk'))
        
        try:
            Vote.objects.create(organizer=self.request.user,voteregs_id=reguser.id)
        except IntegrityError:
            print('already voted')
        else:
            reguser.votes_total=reguser.votes_total-1
            reguser.save()
            


        return super().get(request,*args,**kwargs)                 