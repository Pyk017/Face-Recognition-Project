from typing import List
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, MyForm,UserUpdateForm,ProfileUpdateForm, MyPasswordChangeForm, DescriptionUpdateForm, FaceLoginForm
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, update_session_auth_hash

from .models import Profile
# from .models import userdata
from Passwords.models import PasswordData
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
# Algorithms
from .algorithm import FaceRecognition
from .Algorythm import Capture, Recognize


from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

capture = Capture()
reckon = Recognize()

def addFace(request, face_id):
    result = capture.takePhotos(face_id)
    if not result:
        print('result :- ', result)
        capture.deleteTheDirectory()
        return 'Please Take the photos Again!'
    else:
        capture.invokeTraining()
        return True 


def test(request):
    pro = Profile.objects.last()
    context = {
        'profile': pro
    }    
    if request.method=="POST":
        message = addFace(request, pro.user.username)
        if type(message) == str:
            messages.error(request, message)
            return redirect('detect-face')
        else:    
            messages.success(request, f'PROFILE CREATED!')
        return redirect('login')
    else:
        u_form=DescriptionUpdateForm(request.POST)
        context = { 'profile': pro }


    return render(request, 'fr/detect_face.html', context)
    

def face_recog(request):
    face_name = reckon.recognize()
    print(face_name)
    
    if len(face_name) == 0:
        return False

    _user = User.objects.filter(username=face_name).first()
    # user = profile.user
    print('user', _user)
    if _user:
        login(request, _user)
        return True
    return False


def facelogin(request):
    
    if face_recog(request):
        print('matched')
        # return redirect('profile')
        return redirect('profile')
    
    messages.warning(request, f'You are not an Authorised Person. SignIn First.')
    return redirect('register')


def faceLogin(request):
    if request.method == "POST":
        print('post request activated')    
        return facelogin(request)
    return render(request, 'fr/face_login.html', {})



def register(request):
    if request.method=="POST":
        form=MyForm(request.POST)
        if form.is_valid():
            user = form.save()
            username=form.cleaned_data.get("username")
            print(username, user.id)
            profile = Profile.objects.filter(user_id=user.id).last()
            print("Before:- ", profile.user_secret_key)
            # profile.user_secret_key = Fernet.generate_key().decode('utf-8')
            profile.user_secret_key = AESGCM.generate_key(bit_length=128).decode('latin-1')
            profile.nonce = os.urandom(12).decode('latin-1')
            print('After secret key:- ', profile.user_secret_key)
            print('After nonce:- ', profile.nonce)
            profile.save()

            return redirect('detect-face', permanent=True)
        

    else:
        form=MyForm()
    # form1=signinForm()

    return render(request, 'fr/register.html',{"form":form})


def home(request):
    return render(request, "fr/home.html")


def about(request):
    return render(request, "fr/about.html")

@login_required
def profile(request):
    context={'data': PasswordData.objects.filter(author=request.user)}
    return render(request, 'fr/profile.html', context)

@login_required
def edit_profile(request):
    if request.method=='POST':
        u_form=UserUpdateForm(request.POST, instance=request.user)
        p_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            
            u_form.save()
            p_form.save()
            messages.success(request, f'PROFILE UPDATED')
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
    context={
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'fr/edit_profile.html', context)

@login_required
def edit_password(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        # else:
        #     messages.error(request, 'Please correct the error below.')
    else:
        form = MyPasswordChangeForm(request.user)
    return render(request, 'fr/edit_password.html', {
        'form': form
    })




@login_required
def vault(request):
    return render(request, 'Passwords/vault.html', {})

# Password Mangaer Class Views

# class DataDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):
#     model = userdata
#     def test_func(self):
#         data=self.get_object()
#         if self.request.user==data.author:
#             return True
#         return False

# class DataCreateView(LoginRequiredMixin,CreateView):
#     model=userdata
#     fields=['title', 'userid', 'password', 'link']
#     success_url = '/profile'
#     context_object_name = 'data'
    
#     def form_valid(self,form):
#         form.instance.author=self.request.user
#         return super().form_valid(form)



# class DataUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
#     model=userdata
#     fields=['title', 'userid', 'password', 'link']
#     success_url = '/profile'
#     def form_valid(self,form):
#         form.instance.author=self.request.user
#         return super().form_valid(form)
#     def test_func(self):
#         data=self.get_object()
#         if self.request.user==data.author:
#             return True
#         return False

# class DataDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
#     model=userdata
#     success_url=('/profile')
#     def test_func(self):
#         data=self.get_object()
#         if self.request.user==data.author:
#             return True
#         return False
