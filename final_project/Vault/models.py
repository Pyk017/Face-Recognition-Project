from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

def user_directory_path(instance, filename):
    return 'uploads/{0}/{1}/{2}'.format(instance.user.username, instance.date_created.date(), filename)


class VaultData(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    image=models.ImageField(default='self.request.user.profile.image',upload_to=user_directory_path)
    fileUpload = models.FileField(upload_to=user_directory_path)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=1000, blank=True, default='No Description')



    def __str__(self):
        return f'{self.user.username} {self.description}'   

    def filename(self):
        print(os.path.basename(self.image.name))
        return os.path.basename(self.image.name)

    # def __repr__(self):
    #     return self.user