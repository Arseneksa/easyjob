
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Utilisateur (User):
        diplome = models.CharField(max_length=255)
        specialite = models.CharField(max_length=255)
        Telephone = models.IntegerField()
        competence =  models.CharField(max_length=100)
        localisation =  models.CharField(max_length=100)
        #ecole = models.CharField(max_length=100)
class Job (models.Model):
        category = models.CharField(max_length=100)
        title = models.CharField(max_length=250)
        compagny = models.CharField(max_length=100)
        localisation = models.CharField(max_length=100)
        town = models.CharField(max_length=100)
        region = models.CharField(max_length=100)
        pubdate = models.CharField(max_length=100)
        gender = models.CharField(max_length=100)
        salary = models.CharField(max_length=100)
        description = models.TextField()
class Favoris (models.Model):
        user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE) 
        job = models.ForeignKey(Job, on_delete=models.CASCADE)
        
        
