from django.db import models

# Create your models here.
class Uuid(models.Model):
    text = models.CharField(max_length=100)
    uuid = models.CharField(max_length=100)