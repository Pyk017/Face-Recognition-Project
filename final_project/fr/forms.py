from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from .models import Profile
from cryptography.fernet import Fernet
import re


class MyForm(UserCreationForm):

    error_messages = {
        'password_mismatch': "The two passwords fields didn't match",
        'username_required': "User name is a required field",
        'username_rules': 'User name must not contain any special character aside from space.',
        'valid_images': "Image Uploaded is not in valid form, must be in png or jpg format",
        'password_length': "Your Password is not secure enough, must be at least 8 characters long.",
        'password_security': "Your Password must contain at least 1 number and a capital letter."
    }


    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'username'}), max_length=100,required=True)

    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'placeholder':'email'}), max_length=100, required=True)

    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'password'}),required=True)
    
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}), required=True)

    # password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    # password2 = forms.CharField(max_length=32, widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        help_texts = {
            'username': None,
            'email': None,
            
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        
        if len(password) < 8:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        pattern = '[A-Za-z0-9@#$%^&+=]+'
        result = re.match(pattern, password)
        print(result, pattern, password);
        if not result:
            raise forms.ValidationError(
                self.error_messages['password_security'],
                code = 'password_security'
            )

        return password


    def clean_username(self):
        username=self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(
                self.error_messages['username_required'],
                code='username_required'
            )

        pattern = '^[^0-9][a-zA-Z0-9_ ]+$'
        result = re.match(pattern, username)

        if username and not result:
            raise forms.ValidationError(
                self.error_messages['username_rules'],
                code='username_rules'
            )
        return username


    def save(self, commit=True):
        user = super(MyForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.user_secret_key = Fernet.generate_key().decode('utf-8')

        if commit:
            user.save()
        return user
    

# class signinForm(forms.Form):
#     name = forms.CharField(label='Enter your name', max_length=100)

#     password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label="",widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username', 'id': 'hello'}))
    password = forms.CharField(label="",widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'password',
            'id': 'hi',
            'style': 'display:flex'
        }
))


class FaceLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FaceLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label="",widget=forms.TextInput(
        attrs={'class': 'form-control userInput', 'placeholder': 'username', 'id': 'hello', 'value':""}))



#  feedback = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "20", }))

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'placeholder':'email'}), max_length=100)
    # password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'password'}),required=True)
    
    # password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}), required=True)

    class Meta:
        model=User
        fields=["username","email"]
        help_texts = {
            'username': None,
            'email': None,
            
        }
    
    # def clean(self):
    #     cleaned_data = super(UserUpdateForm, self).clean()
    #     password1 = cleaned_data.get("password1")
    #     password2 = cleaned_data.get("password2")

    #     if password1 != password2:
    #         raise forms.ValidationError(
    #             "password and confirm_password does not match"
    #         )
    

    

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']
        
class DescriptionUpdateForm(forms.ModelForm):
    description = forms.Textarea()
    class Meta:
        model = Profile
        fields=['description']


class MyPasswordChangeForm(PasswordChangeForm,SetPasswordForm):
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    # class Meta:
    #     model=User
    #     fields=['old_password',"new_password1","new_password2"]
