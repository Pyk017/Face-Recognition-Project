from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="fr-home"),
    path('about/', views.about, name="fr-about"),
]