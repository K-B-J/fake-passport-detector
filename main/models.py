from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class modUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    typeOfUser = models.BooleanField(null=False, default=False)
