
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from companies.models import Company, VerksamhetsOmraden, ForetagsStorlek
from .models import Project
import json

@login_required
def project_overview(request, project_id):
    assert isinstance(request, HttpRequest)
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    companies = project.companies.all()  
    return render(
        request,
        'projects/overview.html',
        {
            'title': 'Projektoversikt',
            'message': 'valt projekt.',
            'year': datetime.now().year,
            'project': project,
            'companies': companies,  
        }
    )


@login_required
def project_list(request):
    assert isinstance(request, HttpRequest)
    show_archived = request.GET.get('show_archived', 'false') == 'true'
    if show_archived:
        projects = Project.objects.filter(created_by=request.user)
    else:
        projects = Project.objects.filter(created_by=request.user, archived=False)
    return render(
        request,
        'projects/projectlist.html',
        {
            'title': 'Projektlista',
            'message': 'alla dina projekt.',
            'year': datetime.now().year,
            'projects': projects,
            'show_archived': show_archived,
        }
    )

@login_required
@require_POST
def add_project(request):
    data = json.loads(request.body)
    project_name = data.get('name')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    project = Project.objects.create(name=project_name, start_date=start_date, end_date=end_date, created_by=request.user)

    return JsonResponse({'status': 'success', 'project': {'id': project.id, 'name': project.name}})

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
