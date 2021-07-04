from django import forms
from django.db.models import fields
from .models import VaultData

class UploadFileForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    image = forms.ImageField()

    class Meta:
        model = VaultData
        fields = ['image', 'file', 'title']