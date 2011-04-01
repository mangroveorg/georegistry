#!/usr/bin/env python
from django import forms
from georegistry.accounts.models import *
#from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.contrib.localflavor.us.forms import *
from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile
from django.conf import settings


class RegistrationForm(RegistrationFormUniqueEmail):
    username = forms.CharField(max_length=30, label="Username*")
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password*")
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password(again)*")
    email = forms.EmailField(max_length=75, label="Email*")
    first_name = forms.CharField(max_length=30, label="First Name*")
    last_name = forms.CharField(max_length=30, label="Last Name*")
    organization_name = forms.CharField(max_length=100,  label="Organization Name*")
    mobile_phone_number = forms.CharField(max_length=15, required=False,
                            label="Mobile Phone Number")
    twitter = forms.CharField(max_length=100, required=False,
                            label="Twitter ID")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        if len(password1) < settings.MIN_PASSWORD_LEN:
            msg="Password must be at least %s characters long.  Be tricky!" % (settings.MIN_PASSWORD_LEN)
            raise forms.ValidationError(msg)
        return password2


   

    def save(self, profile_callback=None):
        new_user = RegistrationProfile.objects.create_inactive_user(
                        username=self.cleaned_data['username'],
                        password=self.cleaned_data['password1'],
                        email=self.cleaned_data['email'],
                        profile_callback=profile_callback)
        new_user.first_name = self.cleaned_data.get('first_name', "")
        new_user.last_name = self.cleaned_data.get('last_name', "")
        new_user.save()
        UserProfile.objects.create(
            user=new_user,
            mobile_phone_number=self.cleaned_data.get('mobile_phone_number', ""),
            organization_name=self.cleaned_data.get('organization_name', ""),
            twitter=self.cleaned_data.get('twitter', ""),

            )
        
        return new_user

class AccountSettingsForm(forms.Form):
    organization_name = forms.CharField(max_length=100,  label="Organization Name*")
    mobile_phone_number = forms.CharField(max_length=15, required=False,
                            label="Mobile Phone Number")
    twitter = forms.CharField(max_length=100, required=False, label="Twitter ID")
    


