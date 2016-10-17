from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class InvestUser(AbstractUser):
    """
    모의 투자 유저
    """

    money = models.IntegerField(default=100000)
