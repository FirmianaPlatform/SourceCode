import re
from experiments.models import *
from django import forms
from  django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
#from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label="Password(Again)",
        widget=forms.PasswordInput()
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username/Email has already been taken.')
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Experimenter.objects.get(email=str(email))
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Email has already been taken!')

class ChangepwdForm(forms.Form):
    email = forms.EmailField(label="Email")
    oldpassword = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput()
    )
    newpassword1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput()
    )
    newpassword2 = forms.CharField(
        label="New Password(Again)",
        widget=forms.PasswordInput()
    )
    def clean(self):
        if self.cleaned_data['newpassword1'] <> self.cleaned_data['newpassword2']:
            raise forms.ValidationError(u"New passwords don't match.")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class InvitationForm(forms.Form):
    name = forms.CharField(label='Name')
    email = forms.EmailField(label='Email')
    
class ResetPsdForm(forms.Form):
    email = forms.EmailField(label='Email')

#@login_required(login_url="/login/")
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False, label='Your e-mail address')
    message = forms.CharField(widget=forms.Textarea)
