from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from .models import Profile




class MyForm(UserCreationForm):
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

    # def save(self):
    #     data = self.cleaned_data
    #     user = User(username=data['username'],
    #         email=data['email'], 
    #         password=data['password'],
            
    #         )
    #     user.save()
    

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
