"""
Definition of views.
"""

from datetime import datetime
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from companies.models import Company, VerksamhetsOmraden, ForetagsStorlek
from locations.models import Stad, Lan, Land
from projects.models import Project  # Lägg till denna import

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def administrator(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/administrator.html',
        {
            'title':'Administrator',
            'message':'Redigera data.',
            'year':datetime.now().year,
        }
    )

def projects(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/projects.html',
        {
            'title':'Projekt',
            'message':'Mina projekt.',
            'year':datetime.now().year,
        }
    )

#Skapa projekt
@login_required
@require_POST
def add_project(request):
    data = json.loads(request.body)
    project_name = data.get('name')

    project = Project.objects.create(name=project_name, created_by=request.user)

    return JsonResponse({'status': 'success', 'project': {'id': project.id, 'name': project.name}})


#Koppla företag till projekt
@login_required
@require_POST
def add_companies_to_project(request):
    data = json.loads(request.body)
    project_id = data.get('project_id')
    company_ids = data.get('company_ids')

    project = get_object_or_404(Project, id=project_id, created_by=request.user)

    for company_id in company_ids:
        company = get_object_or_404(Company, id=company_id)
        if not project.companies.filter(id=company_id).exists():
            project.companies.add(company)

    return JsonResponse({'status': 'success'})

#Sök företag
def sok_foretags(request):
    lander = Land.objects.all()
    lan = Lan.objects.prefetch_related('stader').all()
    stader = Stad.objects.all()
    omraden = VerksamhetsOmraden.objects.all()
    storlekar = ForetagsStorlek.objects.all()
    projects = Project.objects.filter(created_by=request.user)  # Hämta alla projekt skapade av den inloggade användaren

    resultat = None

    if request.method == 'GET':
        land = request.GET.get('land', None)
        stader_valda = request.GET.getlist('stad')
        omraden_valda = request.GET.getlist('omrade')
        storlekar_valda = request.GET.getlist('storlek')  # Ändra till getlist för att hantera flera storlekar

        if land or stader_valda or omraden_valda or storlekar_valda:
            resultat = Company.objects.all()

        if land:
            land_obj = Land.objects.filter(id=land).first()
            if land_obj:
                resultat = resultat.filter(verksamma_lander=land_obj)

        if stader_valda:
            try:
                stader_valda_ids = [int(stad) for stad in stader_valda]
                resultat = resultat.filter(verksamma_stader__id__in=stader_valda_ids)
            except ValueError:
                resultat = None

        if omraden_valda:
            resultat = resultat.filter(omraden__id__in=omraden_valda).distinct()

        if storlekar_valda:
            resultat = resultat.filter(storlek_id__in=storlekar_valda).distinct()

        if resultat:
            resultat = resultat.distinct()

    context = {
        'lander': lander,
        'lan': lan,
        'stader': stader,
        'omraden': omraden,
        'storlekar': storlekar,
        'projects': projects,
        'resultat': resultat,
    }

    return render(request, 'app/sok.html', context)



