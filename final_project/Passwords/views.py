from django.conf.urls import url
from django.http import request, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from fr.models import userdata

from .models import PasswordData
from fr.AES_OOP import AES

import qrcode
import qrcode.image.svg
from io import BytesIO


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

        # User's personal secret key and nonce
        secret_key = (self.request.user.profile.user_secret_key).encode('latin-1')
        nonce = (self.request.user.profile.nonce).encode('latin-1')

        # Object of self defined AES class implementing AES Algorithm using cryptography module
        aes = AES(secret_key)
        # Encrypted Password 
        token = context['data'].password

        # Decryption Process
        decrypted_text, by = aes.decrypt(nonce, token)
        print('Decrypted_Text :- ' ,decrypted_text)
        print('Decrypted_Text in bytes :- ' ,by)
        
        # Decrypted Password
        context['form_input'] = decrypted_text
        
        # QR code generation
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(context['form_input'], image_factory=factory, box_size=35)
        stream = BytesIO()
        img.save(stream)
        context['svg'] = stream.getvalue().decode()

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

        # User's personal secret key and nonce
        secret_key = (self.request.user.profile.user_secret_key).encode('latin-1')
        nonce = (self.request.user.profile.nonce).encode('latin-1')

        # Object of self defined AES class implementing AES Algorithm using cryptography module
        aes = AES(secret_key)

        # Getting Password from Form
        enc_string = form_data['password']
    
        # Encryption Process
        encoded_text, by = aes.encrypt(nonce, enc_string)
        print("Encoded text = ", encoded_text)
        print('in bytes :- ', by)
        print("nonce :- ", nonce)
        
        # Changing the form instance to save the encrypted password rather than raw password
        form.instance.password = encoded_text
        
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