from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    user_secret_key = models.CharField("User Secret Key", max_length=500, blank=True, null=True)
    nonce = models.CharField("Nonce", max_length=100, blank=True, null=True)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')
    description = models.TextField(default='nothing in it')

    def __str__(self):
        return f'{self.user.username} Profile'


# class userdata(models.Model):
#     title=models.CharField(max_length=100)
#     userid=models.CharField(max_length=100)
#     password=models.CharField(max_length=100)
#     link=models.CharField(max_length=1000, blank=True, default='')
#     date_created=models.DateTimeField(default=timezone.now)
#     author= models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title