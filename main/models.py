from django.db import models
from django.contrib.auth.models import User


class Airports(models.Model):
    airport = models.CharField(max_length=255)


class Issuer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()


class Verifier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    airport = models.ForeignKey(Airports, on_delete=models.DO_NOTHING)


class Security(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    airport = models.ForeignKey(Airports, on_delete=models.DO_NOTHING)


class FakePassportReport(models.Model):
    verifier = models.ForeignKey(Verifier, on_delete=models.DO_NOTHING)
    airport = models.ForeignKey(Airports, on_delete=models.DO_NOTHING)
    time = models.CharField(max_length=255)
    passNum = models.CharField(max_length=255)
    image = models.URLField(max_length=255)
    options = models.CharField(max_length=255)
    remarks = models.TextField()
