from django.db import reset_queries
from django.shortcuts import render, redirect
from .models import VaultData

from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Message Mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages




class VaultListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = VaultData
    template_name = "Vault/vault_list.html"
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super(VaultListView, self).get_context_data(**kwargs)
        context['data'] = context['data'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            print(type(context['data']))
            context['data'] = context['data'].filter(description__icontains=search_input)

        context['search_input'] = search_input
        
        
        for content in context['data']:
            content.fileUpload_name = self.get_filename(str(content.fileUpload))
            content.image_name = self.get_filename(str(content.image))

        

        sort_data = self.request.GET.get('sort') or ''
        print(self.request.GET, sort_data)
        if sort_data:
            if sort_data.startswith('description'):
                if sort_data == 'description_inc':
                    message = 'Description in Dictionary Order'
                    context['data'] = sorted(context['data'], key=lambda x: x.description)
                else:
                    message = 'Description in Reverse Dictionary Order'
                    context['data'] = sorted(context['data'], key=lambda x: x.description)[::-1]
            else:
                if sort_data == 'date_inc':
                    message = 'Least Recently Added'
                    context['data'] = sorted(context['data'], key=lambda x: x.date_created)
                else:
                    message = 'Most Recently Added'
                    context['data'] = sorted(context['data'], key=lambda x: x.date_created)[::-1]
        
            messages.add_message(self.request, messages.SUCCESS, f'Successfully Sorted by - {message}')

        return context


    def get_filename(self, file):
        return file.split('/')[-1]


class VaultCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = VaultData
    fields = ['image', 'fileUpload', 'description']
    template_name = 'Vault/vault_upload.html'
    context_object_name = 'data'
    success_url =  reverse_lazy("vault-list")
    success_message = '%(description)s Added successfully'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class VaultDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = VaultData
    success_url = reverse_lazy("vault-list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

