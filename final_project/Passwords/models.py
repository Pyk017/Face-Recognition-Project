from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PasswordData(models.Model):
    site_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    link = models.CharField(max_length=1000, blank=True, default='')
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.site_name