"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from fr import views as fr_views
from django.contrib.auth import views as auth_views
from fr.forms import FaceLoginForm, LoginForm
from django.conf import settings
from django.conf.urls.static import static
from fr.views import FaceLoginForm
from fr.views import DataDetailView, DataCreateView, DataUpdateView, DataDeleteView

# from fr.views import ProfileView

# print(ProfileView.model)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', fr_views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='fr/login.html', authentication_form=LoginForm), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='fr/logout.html'), name="logout"),
    path('profile/', fr_views.profile, name="profile"),
    path('edit_profile/', fr_views.edit_profile, name="edit_profile"),
    path('', include('fr.urls')),
    # path('detect-face/', ProfileView.as_view(), name="detect-face"),
    path('face_login/', fr_views.faceLogin, name="face-login"),
    path('detect-face/', fr_views.test, name="detect-face"),


    path('data/<int:pk>/', DataDetailView.as_view(), name="data-detail"),
    path('data/create/', DataCreateView.as_view(), name="data-create"),
    path('data/<int:pk>/update', DataUpdateView.as_view(), name="data-update"),
    path('data/<int:pk>/delete', DataDeleteView.as_view(), name="data-delete"),

    # path(
    #     'edit_password/',
    #     auth_views.PasswordChangeView.as_view(
    #         template_name='fr/edit_password.html',
    #         success_url = '/profile'
    #     ),
    #     name='edit_password'
    # ),

    path('edit_password/', fr_views.edit_password, name="edit_password")
    
]



if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
