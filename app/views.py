"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from companies.models import Company, VerksamhetsOmraden, ForetagsStorlek
from locations.models import Stad, Lan, Land
from projects.models import Project
from django.views.decorators.csrf import csrf_exempt
import json

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

def company_list(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/company_list.html',
        {
            'title':'company_list',
            'message':'Your application company_list page.',
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
        'app/projects222.html',
        {
            'title':'Projekt',
            'message':'Mina projekt222.',
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


#Koppla foretag till projekt
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

#Sok foretag
def sok_foretags(request):
    lander = Land.objects.all()
    lan = Lan.objects.prefetch_related('stader').all()
    stader = Stad.objects.all()
    omraden = VerksamhetsOmraden.objects.all()
    storlekar = ForetagsStorlek.objects.all()
    projects = Project.objects.filter(created_by=request.user)  # Hamta alla projekt skapade av den inloggade anvandaren

    resultat = None

    if request.method == 'GET':
        land = request.GET.get('land', None)
        stader_valda = request.GET.getlist('stad')
        omraden_valda = request.GET.getlist('omrade')
        storlekar_valda = request.GET.getlist('storlek')  # andra till getlist for att hantera flera storlekar

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

def company_list(request):
    # Fetch companies sorted by Area (omraden) and then by Name (namn)
    companies = Company.objects.prefetch_related('omraden', 'verksamma_stader').order_by('omraden__sorteringsordning', 'namn')
    omraden = VerksamhetsOmraden.objects.all()  # Fetch all available areas
    counties = Lan.objects.prefetch_related('stader').all()  # Fetch counties with their cities

    for company in companies:
        company.omraden_ids = list(company.omraden.values_list('id', flat=True))  # Preprocess area IDs
        company.city_ids = list(company.verksamma_stader.values_list('id', flat=True))  # Preprocess city IDs

    return render(request, 'app/company_list.html', {
        'companies': companies,
        'omraden': omraden,
        'counties': counties,  # Pass counties and their cities
    })

@csrf_exempt
def add_company(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        company = Company.objects.create(
            namn=data.get('namn'),
            epost=data.get('epost'),
            telefonnummer=data.get('telefonnummer'),
            konkurs=data.get('konkurs', False)
        )
        company.omraden.set(data.get('omraden', []))  # Use .set() for many-to-many field
        company.verksamma_stader.set(data.get('verksamma_stader', []))  # Use .set() for many-to-many field
        return JsonResponse({'id': company.id}, status=201)


@csrf_exempt
def edit_company(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            company_id = data.get('id')
            company = Company.objects.get(id=company_id)

            # Update company fields
            company.namn = data.get('namn', company.namn)
            company.epost = data.get('epost', company.epost)
            company.telefonnummer = data.get('telefonnummer', company.telefonnummer)
            company.konkurs = data.get('konkurs', company.konkurs)

            # Update related fields
            omraden_ids = data.get('omraden', [])
            company.omraden.set(VerksamhetsOmraden.objects.filter(id__in=omraden_ids))

            city_ids = data.get('cities', [])
            company.verksamma_stader.set(Stad.objects.filter(id__in=city_ids))

            company.save()
            return JsonResponse({'success': True, 'message': 'Company updated successfully.'})
        except Company.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Company not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


@csrf_exempt
def delete_company(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("Received ID for deletion:", data.get('id'))  # Log the received ID
        company = get_object_or_404(Company, id=data.get('id'))
        company.delete()
        return JsonResponse({'status': 'success'}, status=200)

import pandas as pd
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('excelFile'):
        excel_file = request.FILES['excelFile']
        file_path = default_storage.save(f'temp/{excel_file.name}', excel_file)

        try:
            # Read the Excel file and use the first row as headers
            excel_data = pd.read_excel(default_storage.open(file_path), header=0)

            # Log column headers for debugging
            print("Column headers:", excel_data.columns.tolist())

            for _, row in excel_data.iterrows():
                # Handle VerksamhetsOmraden
                sorteringsordning = row['A']  # Ensure 'A' matches the actual column name
                omrade, created = VerksamhetsOmraden.objects.get_or_create(
                    sorteringsordning=sorteringsordning,
                    defaults={'namn': str(sorteringsordning)}
                )

                # Handle Company
                company, created = Company.objects.get_or_create(
                    namn=row['B'],  # Ensure 'B' matches the actual column name
                    defaults={
                        'organisationsnummer': row['C'],
                        'kontaktperson': f"{row['D']} {row['E']}".strip(),
                        'telefonnummer': row['F'],
                        'epost': row['G']
                    }
                )
                company.omraden.add(omrade)

                # Handle Cities (H-M)
                if pd.notna(row['H']):  # Check if the cell is not empty
                    company.verksamma_stader.add(Stad.objects.get(namn='Malmö'))
                    company.verksamma_stader.add(Stad.objects.get(namn='Lund'))
                if pd.notna(row['I']):  # Check if the cell is not empty
                    company.verksamma_stader.add(Stad.objects.get(namn='Helsingborg'))
                if pd.notna(row['J']):  # Check if the cell is not empty
                    company.verksamma_stader.add(Stad.objects.get(namn='Halmstad'))
                if pd.notna(row['K']):  # Check if the cell is not empty
                    company.verksamma_stader.add(Stad.objects.get(namn='Varberg'))
                if pd.notna(row['L']):  # Check if the cell is not empty
                    company.verksamma_stader.add(Stad.objects.get(namn='Växjö'))
                if pd.notna(row['M']):  # Check if the cell is not empty
                    company.verksamma_stader.add(Stad.objects.get(namn='Kalmar'))

            return JsonResponse({'status': 'success', 'message': 'Data processed successfully.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f"Missing column: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'No file uploaded.'}, status=400)


def area_list(request):
    """Renders the area list page."""
    areas = VerksamhetsOmraden.objects.all().order_by('sorteringsordning', 'namn')
    return render(request, 'app/area_list.html', {
        'areas': areas,
    })

@csrf_exempt
def add_area(request):
    """Handles adding a new area."""
    if request.method == 'POST':
        data = json.loads(request.body)
        area = VerksamhetsOmraden.objects.create(
            sorteringsordning=data.get('sorteringsordning'),
            namn=data.get('namn'),
            ikon=data.get('ikon'),
            farg_css_klass=data.get('farg_css_klass')
        )
        return JsonResponse({'id': area.id}, status=201)

@csrf_exempt
def edit_area(request):
    """Handles editing an existing area."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Edit Request Data:", data)  # Debug log
            area_id = data.get('id')
            area = VerksamhetsOmraden.objects.get(id=area_id)

            # Update area fields
            area.sorteringsordning = data.get('sorteringsordning', area.sorteringsordning)
            area.namn = data.get('namn', area.namn)
            area.ikon = data.get('ikon', area.ikon)
            area.farg_css_klass = data.get('farg_css_klass', area.farg_css_klass)
            area.save()

            return JsonResponse({'success': True, 'message': 'Area updated successfully.'})
        except VerksamhetsOmraden.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Area not found.'}, status=404)
        except Exception as e:
            print("Error in edit_area:", str(e))  # Debug log
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def delete_area(request):
    """Handles deleting an area."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Delete Request Data:", data)  # Debug log
            area = get_object_or_404(VerksamhetsOmraden, id=data.get('id'))
            area.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            print("Error in delete_area:", str(e))  # Debug log
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)








