from base64 import encode
from django.conf.urls import url
from django.http import request, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from fr.models import userdata
from .models import PasswordData
from fr.models import Profile
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

import qrcode
import qrcode.image.svg
from io import BytesIO

nonce = os.urandom(12)


class PasswordListView(LoginRequiredMixin, ListView):
    model = PasswordData
    template_name = 'Passwords/passwords_list.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super(PasswordListView, self).get_context_data(**kwargs)
        context['data'] = context['data'].filter(author=self.request.user)
        context['count'] = context['data'].filter(author=self.request.user).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['data'] = context['data'].filter(site_name__icontains=search_input)

        context['search_input'] = search_input

        return context


class PasswordDetailView(LoginRequiredMixin, DetailView):
    model = PasswordData
    context_object_name = 'data'
    template_name = 'Passwords/password_details.html'

    def get_context_data(self, **kwargs):
        context = super(PasswordDetailView, self).get_context_data(**kwargs)

        secret_key = (self.request.user.profile.user_secret_key).encode('utf-8')
        _cipher = Fernet(secret_key)
        # _cipher = AESGCM(secret_key)
        # nonce = os.urandom(12)
        token = context['data'].password.encode('utf-8')
        # print('token :- ', token)
        # print('typeoftoken :- ', type(token))
        # nonce = os.urandom(12)
        # print('nonce :- ', nonce)
        # print('type of nonce :- ', type(nonce))
        decrypt = _cipher.decrypt(token)
        context['form_input'] = decrypt.decode('utf-8')

        
        # QR code generation

        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(context['form_input'], image_factory=factory, box_size=35)
        stream = BytesIO()
        img.save(stream)
        context['svg'] = stream.getvalue().decode()


        # token = (context['data'].password).encode()
        # decrypt = _cipher.decrypt(token)
        # context['data'].password = decrypt
        return context


    


class PasswordCreateView(LoginRequiredMixin,CreateView):
    model = PasswordData
    fields = ['site_name', 'user_id', 'password', 'link']
    template_name = 'Passwords/add_new_password.html'
    success_url = reverse_lazy('passwords-list')
    context_object_name = 'data'

    def form_valid(self,form):
        form.instance.author=self.request.user
        form_data = form.cleaned_data
        secret_key = (self.request.user.profile.user_secret_key).encode('utf-8')
        # _cipher = Fernet(secret_key)
        _cipher = AESGCM(secret_key)
        enc_string = form_data['password']
        nonce = os.urandom(12)
        # encoded_text = _cipher.encrypt(str.encode(enc_string))
        encoded_text = _cipher.encrypt(enc_string.encode('utf-8'))

        # new_pass = PasswordData(
        #     site_name = form_data['site_name'],
        #     password = encoded_text.decode('utf-8'),
        #     user_id = form_data['user_id'],
        #     link = form_data['link'],
        #     author = self.request.user
        # )
        # new_pass.save()

        form.instance.password = encoded_text.decode('utf-8')
        print('encoded-text :- ', encoded_text)
        print("encoded encoded-text :- ", encoded_text.decode("latin-1"))

        # print('Encoded string :- ', encoded_text)
        # decoded_text = encoded_text.decode('utf-8')
        # print('Decoded string :- ', decoded_text)
        # return HttpResponse('password-manager')
        return super().form_valid(form)



class PasswordUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = PasswordData
    fields = ['site_name', 'user_id', 'password', 'link']
    success_url = reverse_lazy('passwords-list')
    template_name = "Passwords/add_new_password.html"
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        data=self.get_object()
        if self.request.user==data.author:
            return True
        return False


class PasswordDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = PasswordData
    success_url = reverse_lazy('passwords-list')
    template_name = 'Passwords/password_delete_confirmation.html'

    def test_func(self):
        data=self.get_object()
        if self.request.user==data.author:
            return True
        return False