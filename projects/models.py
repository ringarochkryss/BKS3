from django.db import models
from django.contrib.auth.models import User
from companies.models import Company

class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    companies = models.ManyToManyField(Company, blank=True)

    def __str__(self):
        return self.name