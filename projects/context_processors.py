from .models import Project
from companies.models import Company

def project_list(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(created_by=request.user)
        companies = Company.objects.filter(project__created_by=request.user).distinct()
    else:
        projects = Project.objects.none()
        companies = Company.objects.none()
    return {'projects': projects, 'companies': companies}
