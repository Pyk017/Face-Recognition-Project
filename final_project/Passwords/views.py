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

class PasswordListView(LoginRequiredMixin, ListView):
    model = PasswordData
    template_name = 'Passwords/passwords_list.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super(PasswordListView, self).get_context_data(**kwargs)
        context['data'] = context['data'].filter(author=self.request.user)
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

        secret_key = (self.request.user.profile.user_secret_key).encode()
        _cipher = Fernet(secret_key)
        token = str(context['data'].password).encode()
        decrypt = _cipher.decrypt(token)
        context['form_input'] = str(decrypt.decode())

        
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
        secret_key = (self.request.user.profile.user_secret_key).encode()
        _cipher = Fernet(secret_key)
        enc_string = form_data['password']
        encoded_text = _cipher.encrypt(str.encode(enc_string))

        # new_pass = PasswordData(
        #     site_name = form_data['site_name'],
        #     password = encoded_text.decode('utf-8'),
        #     user_id = form_data['user_id'],
        #     link = form_data['link'],
        #     author = self.request.user
        # )
        # new_pass.save()

        form.instance.password = encoded_text.decode('utf-8')

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