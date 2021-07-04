from django.db import reset_queries
from django.shortcuts import render, redirect
from .models import VaultData

from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.\



class VaultListView(LoginRequiredMixin, ListView):
    model = VaultData
    template_name = "Vault/vault_list.html"
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super(VaultListView, self).get_context_data(**kwargs)
        context['data'] = context['data'].filter(user=self.request.user)[::-1]

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            print(type(context['data']))
            context['data'] = context['data'].filter(description__icontains=search_input)

        context['search_input'] = search_input
        
        
        for content in context['data']:
            content.fileUpload_name = self.get_filename(str(content.fileUpload))
            content.image_name = self.get_filename(str(content.image))

            

        return context


    def get_filename(self, file):
        return file.split('/')[-1]


class VaultCreateView(LoginRequiredMixin, CreateView):
    model = VaultData
    fields = ['image', 'fileUpload', 'description']
    template_name = 'Vault/vault_upload.html'
    context_object_name = 'data'
    success_url =  reverse_lazy("vault-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



