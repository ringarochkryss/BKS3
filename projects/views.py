from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from companies.models import Company, VerksamhetsOmraden, ForetagsStorlek
from .models import Project, ProjectCompany, Status  # Lägg till Status importen
import json

@login_required
def project_overview(request, project_id):
    assert isinstance(request, HttpRequest)
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    companies = project.companies.all()
    statuses = Status.objects.all()  # Hämta alla statusar
    return render(
        request,
        'projects/overview.html',
        {
            'title': 'Projektoversikt',
            'message': 'valt projekt.',
            'year': datetime.now().year,
            'project': project,
            'companies': companies,
            'statuses': statuses,  # Lägg till statusar i contexten
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

    
@login_required
def project_overview(request, project_id):
    assert isinstance(request, HttpRequest)
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    companies = project.companies.all()
    statuses = Status.objects.all()  # Hämta alla statusar
    
    # Skapa en lista med företag och deras status
    company_status_list = []
    for company in companies:
        project_company = ProjectCompany.objects.filter(project=project, company=company).first()
        company_status_list.append({
            'company': company,
            'status': project_company.status if project_company else None
        })
    
    return render(
        request,
        'projects/overview.html',
        {
            'title': 'Projektoversikt',
            'message': 'valt projekt.',
            'year': datetime.now().year,
            'project': project,
            'companies': companies,
            'statuses': statuses,  # Lägg till statusar i contexten
            'company_status_list': company_status_list,  # Lägg till company_status_list i contexten
        }
    )





@login_required
@require_POST
def update_status(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    for company in project.companies.all():
        status_id = request.POST.get(f'status_{company.id}')
        if status_id:
            status = get_object_or_404(Status, id=status_id)
            ProjectCompany.objects.update_or_create(
                project=project,
                company=company,
                defaults={'status': status}
            )
    return redirect('project_overview', project_id=project_id)




