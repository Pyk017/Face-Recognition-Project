from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from fr.models import userdata
from .models import PasswordData


class PasswordListView(LoginRequiredMixin, ListView):
    model = PasswordData
    template_name = 'Passwords/passwords_list.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['data'] = context['data'].filter(site_name__icontains=search_input)

        context['search_input'] = search_input
        return context


class PasswordDetailView(LoginRequiredMixin, DetailView):
    model = PasswordData
    template_name = 'Passwords/password_details.html'


class PasswordCreateView(LoginRequiredMixin,CreateView):
    model = PasswordData
    fields = ['site_name', 'user_id', 'password', 'link']
    template_name = 'Passwords/add_new_password.html'
    success_url = '/password-manager'
    context_object_name = 'data'

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)


class PasswordUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = PasswordData
    fields = ['site_name', 'user_id', 'password', 'link']
    success_url = '/password-manager'
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
    success_url = '/password-manager'
    template_name = 'Passwords/password_delete_confirmation.html'

    def test_func(self):
        data=self.get_object()
        if self.request.user==data.author:
            return True
        return False