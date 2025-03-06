from django.db import models

class Land(models.Model):
    namn = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.namn


class Lan(models.Model):
    namn = models.CharField(max_length=100)
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name='lan')

    def __str__(self):
        return f"{self.namn}, {self.land.namn}"


class Stad(models.Model):
    namn = models.CharField(max_length=100)
    lan = models.ForeignKey(Lan, on_delete=models.CASCADE, related_name='stader')

    def __str__(self):
        return f"{self.namn}, {self.lan.namn}"
