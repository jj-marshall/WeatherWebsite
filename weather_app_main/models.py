from django.db import models

class Location_Data(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
