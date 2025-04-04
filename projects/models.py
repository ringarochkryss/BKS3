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
    share_with_colleagues = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CompanyProjectStatus(models.TextChoices):
    SENT_INQUIRY = 'SentInquiry', 'Sent Inquiry'
    ANSWERED_NO = 'AnsweredNo', 'Answered No'
    ANSWERED_YES = 'AnsweredYes', 'Answered Yes'
    SUBMITTED = 'Submitted', 'Submitted'

class MyCompanyContact(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contacts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    roll = models.CharField(max_length=100)
    namn = models.CharField(max_length=200)
    telefon = models.CharField(max_length=20)
    email = models.EmailField()
    kommentar = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.namn

class MyContactInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    roll = models.CharField(max_length=100)
    namn = models.CharField(max_length=200)
    telefon = models.CharField(max_length=20)
    email = models.EmailField()
    kommentar = models.TextField(blank=True, null=True)