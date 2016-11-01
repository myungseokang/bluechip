from django.db import models

# Create your models here.
class Term(models.Model):
    term = models.CharField(max_length=100, unique=True)
    mean = models.CharField(max_length=1000)
