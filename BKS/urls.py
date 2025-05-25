"""
Definition of urls for BKS.
"""

from datetime import datetime
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from app.views import upload_excel_areas
from projects import views as project_views 

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('administrator/', views.administrator, name='administrator'),
    #Search views
    path('projects/', views.administrator, name='projects222'),
    path('sok/', views.sok_foretags, name='sok_foretags'),
    path('add_companies_to_project/', views.add_companies_to_project, name='add_companies_to_project'),
    path('add_project/', views.add_project, name='add_project'),
    
    #Project views
    path('projects/overview/<int:project_id>/', project_views.project_overview, name='project_overview'),
    path('projects/list/', project_views.project_list, name='project_list'), 
    path('edit_project/', project_views.edit_project, name='edit_project'),
    path('delete_project/', project_views.delete_project, name='delete_project'),
    path('add_project/', project_views.add_project, name='add_project'),
    path('projects/<int:project_id>/update_status/', project_views.update_status, name='update_status'),

    #Admin views
    path('admin/', admin.site.urls),
    path('company_list/', views.company_list, name='company_list'),
    path('administrator/', views.administrator, name='admin'), 
   
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

    #Company List
    path('companies/', views.company_list, name='company_list'),
    path('companies/add/', views.add_company, name='add_company'),
    path('companies/edit/', views.edit_company, name='edit_company'),
    path('companies/delete/', views.delete_company, name='delete_company'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),

    #Area List
    path('areas/', views.area_list, name='area_list'),
    path('add_area/', views.add_area, name='add_area'),
    path('edit_area/', views.edit_area, name='edit_area'),
    path('delete_area/', views.delete_area, name='delete_area'),
    path('upload_excel_areas/', upload_excel_areas, name='upload_excel_areas'),

]