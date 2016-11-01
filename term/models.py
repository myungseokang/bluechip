from django.db import models


class Term(models.Model):
    term = models.CharField(max_length=100, unique=True)
    mean = models.CharField(max_length=1000)

    def __str__(self):
        return self.term
