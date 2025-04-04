from django.db import models
from locations.models import Stad, Land  # Importera Stad och Land från locations-appen

class ForetagsStorlek(models.Model):
    namn = models.CharField(max_length=100)
    ikon = models.CharField(max_length=100, blank=True, null=True)
    farg_css_klass = models.CharField(max_length=100, blank=True, null=True)
    sorteringsordning = models.IntegerField()

    def __str__(self):
        return self.namn


class VerksamhetsOmraden(models.Model):
    namn = models.CharField(max_length=100)
    ikon = models.CharField(max_length=100, blank=True, null=True)
    farg_css_klass = models.CharField(max_length=100, blank=True, null=True)
    sorteringsordning = models.IntegerField()

    def __str__(self):
        return self.namn


class Company(models.Model):
    namn = models.CharField(max_length=200)
    epost = models.EmailField(blank=True, null=True)
    telefonnummer = models.CharField(max_length=20, blank=True, null=True)
    hemsida = models.URLField(blank=True, null=True)
    kontaktperson = models.CharField(max_length=100, blank=True, null=True)

    # Location
    verksamma_stader = models.ManyToManyField(Stad, blank=True)
    verksamma_lander = models.ManyToManyField(Land, blank=True)

   # Size
    storlek = models.ForeignKey(ForetagsStorlek, on_delete=models.CASCADE, blank=True, null=True)

    # Verksamhetsområden
    omraden = models.ManyToManyField(VerksamhetsOmraden, blank=True)
    kategoriBransch = models.CharField(max_length=100, blank=True, null=True)
    # Bilder
    logotype = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    bild1 = models.ImageField(upload_to='company_images/', blank=True, null=True)
  

    # Texter
    payoff = models.CharField(max_length=300, blank=True, null=True)
    text1 = models.TextField(blank=True, null=True)
    text2 = models.TextField(blank=True, null=True)

    # Booleans
    kund = models.BooleanField(default=False)
    underleverantor = models.BooleanField(default=False)
    konkurs = models.BooleanField(default=False)

    # Invoice
    organisationsnummer = models.CharField(max_length=50, blank=True, null=True)
    adress = models.CharField(max_length=200, blank=True, null=True)

    # Payment Information
    betald = models.BooleanField(default=False)
    betald_datum = models.DateField(blank=True, null=True)
    betalning_utgangsdatum = models.DateField(blank=True, null=True)

    # Update and Boost Info
    uppdaterad_datum = models.DateTimeField(auto_now=True)
    boost = models.BooleanField(default=False)
    super_boost = models.BooleanField(default=False)
    boost_startdatum = models.DateTimeField(blank=True, null=True)
    boost_slutdatum = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.namn

class Account(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='project_numbers')
    omrade = models.ForeignKey(VerksamhetsOmraden, on_delete=models.CASCADE, related_name='project_numbers')
    account = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.company.namn} - {self.omrade.namn}: {self.project_number}"