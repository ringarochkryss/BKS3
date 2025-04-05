from django.contrib import admin
from .models import Project, Status, ProjectCompany, MyCompanyContact, MyContactInfo

admin.site.register(Project)
admin.site.register(Status)
admin.site.register(ProjectCompany)
admin.site.register(MyCompanyContact)
admin.site.register(MyContactInfo)

