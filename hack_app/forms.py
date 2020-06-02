from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
from .models import *
from captcha.fields import ReCaptchaField

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class EditProfileForm(UserChangeForm):
    # template_name='/something/else'

    class Meta:
        model = User
        fields = ('email','first_name','last_name',)




class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,widget=forms.TextInput({'class': 'form-control','placeholder': 'User name'}))
    password = forms.CharField(label=("Password"),widget=forms.PasswordInput({'class': 'form-control','placeholder':'Password'}))

class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField( public_key='6LcWbP4UAAAAAJIt5HsVeGD4qocq1g07Cyv0-SQ5',
    private_key='6LcWbP4UAAAAAM_Wk1GzgO_TfmJk-Z6WMoEG_rpv',)

# travel reimbursement form
class TravelReimbursementForm(forms.ModelForm):
    class Meta():
        model=TravelReimbursement
        fields=['travel_date','from_place','to_place','total_fare','upload_bill']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
# reg forms 

class RegForm1(forms.ModelForm):
    class Meta():
        model=RegModel
        fields=['city','country','company','gender']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['company'].label='Company/College'


class RegForm2(forms.ModelForm):
    class Meta():
        model=RegModel
        fields=['signup_as','student_id','emp_opportunity','learn_ab_hackathon','github_url','how_contribute']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['signup_as'].label='Sign Up As'
        self.fields['student_id'].label='I have a Student ID'        
        self.fields['emp_opportunity'].label='I am interested in employment opportunities'        
        self.fields['learn_ab_hackathon'].label='I learned about hackathon from'        
        self.fields['github_url'].label='Github URL'        
        self.fields['how_contribute'].label='Please tell us about your core strengths and how you can contribute to a Team '   
