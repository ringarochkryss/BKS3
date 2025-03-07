# projects/views.py
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Project
import json

def project_overview(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'projects/overview.html',
        {
            'title': 'Projektoversikt',
            'message': 'valt projekt.',
            'year': datetime.now().year,
        }
    )

@login_required
def project_list(request):
    assert isinstance(request, HttpRequest)
    projects = Project.objects.filter(created_by=request.user)  # Filtrera projekt baserat på inloggad användare
    return render(
        request,
        'projects/projectlist.html',
        {
            'title': 'Projektlista',
            'message': 'alla dina projekt.',
            'year': datetime.now().year,
            'projects': projects,  # Skicka projekten till mallen
        }
    )

@login_required
@require_POST
def edit_project(request):
    data = json.loads(request.body)
    project_id = data.get('id')
    project_name = data.get('name')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    archived = data.get('archived')

    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    project.name = project_name
    project.start_date = start_date
    project.end_date = end_date
    project.archived = archived
    project.save()

    return JsonResponse({'status': 'success', 'project': {'id': project.id, 'name': project.name}})

@login_required
@require_POST
def delete_project(request):
    data = json.loads(request.body)
    project_id = data.get('id')

    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    project.delete()

    return JsonResponse({'status': 'success'})
