"""
Definition of urls for BKS.
"""

from datetime import datetime
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('administrator/', views.administrator, name='administrator'),
    path('projects/', views.administrator, name='projects'),
    path('sok/', views.sok_foretags, name='sok_foretags'),
    path('add_companies_to_project/', views.add_companies_to_project, name='add_companies_to_project'),
    path('add_project/', views.add_project, name='add_project'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
