from typing import List
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, MyForm,UserUpdateForm,ProfileUpdateForm, MyPasswordChangeForm, DescriptionUpdateForm, FaceLoginForm
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, update_session_auth_hash

from django.views.generic.edit import UpdateView
from .models import Profile
from django.urls import reverse_lazy

from .algorithm import FaceRecognition

from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate

facerecognition = FaceRecognition()

def addFace(face_id):
    facerecognition.faceDetect(face_id)
    facerecognition.trainFace()
    return redirect('login')


def test(request):
    pro = Profile.objects.last()
    context = {
        'profile': pro
    }    
    if request.method=="POST":
        addFace(pro.id)
        messages.success(request, f'PROFILE UPDATED')

        return redirect('login')
    else:
        u_form=DescriptionUpdateForm(request.POST)
        context = { 'profile': pro }


    return render(request, 'fr/detect_face.html', context)
    

def face_recog(request):
    face_id = facerecognition.recognizeFace()
    print(face_id)
    profile = Profile.objects.filter(id=face_id).first()
    user = profile.user
    if user:
        login(request, user)
        return True
    return False


def facelogin(request):
    
    if face_recog(request):
        return redirect('profile')
    
    return redirect('login')


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
            messages.success(request, f'{username}: your account has been created, you can now login')
            # return render(request, "fr/detect_face.html", {'user':  username})
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
    return render(request, 'fr/profile.html')

@login_required
def edit_profile(request):
    if request.method=='POST':
        u_form=UserUpdateForm(request.POST, instance=request.user)
        p_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        # p1=u_form.get("password1")
        # p2=u_form.get("password2")
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



