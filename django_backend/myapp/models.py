from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

class UserData(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20, null=True)
    highscore = models.FloatField(validators=[MaxValueValidator(99999)], default = 0)
    most_aliens_killed_in_one_game = models.FloatField(validators=[MaxValueValidator(99999)], default = 0)
