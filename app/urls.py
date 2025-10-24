"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# app/urls.py (or wherever your main urls.py is)
from django.contrib import admin
from django.urls import path, include  # Add include
from django.contrib.auth import views as auth_views
from .views import home, lista_apolices 
from django.conf.urls.static import static
from django.conf import settings
from . import views


# Admin headers
admin.site.site_header = "GS INIMA BRASIL"
admin.site.site_title = "GS INIMA BRASIL"
admin.site.index_title = "GS INIMA BRASIL"

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth - Use these OR include accounts urls, but not both
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Home page
    path('', home, name='home'),
    path('apolices/', lista_apolices, name='lista_apolices'),
    path('apolices/nova/', views.nova_apolice, name='nova_apolice'),
    path('apolices/editar/', views.editar_apolice, name='editar_apolice'),
    path('apolices/<int:apolice_id>/dados/', views.apolice_dados, name='apolice_dados'),

    
    # If you have an accounts app with other views, include it like this:
    # path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)