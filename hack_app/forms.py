from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User
from django import forms
from captcha.fields import ReCaptchaField


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,widget=forms.TextInput({'class': 'form-control','placeholder': 'User name'}))
    password = forms.CharField(label=("Password"),widget=forms.PasswordInput({'class': 'form-control','placeholder':'Password'}))


class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField( public_key='6LcWbP4UAAAAAJIt5HsVeGD4qocq1g07Cyv0-SQ5',
    private_key='6LcWbP4UAAAAAM_Wk1GzgO_TfmJk-Z6WMoEG_rpv',)

