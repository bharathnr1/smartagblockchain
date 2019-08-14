from django.db import models
from django.utils import timezone
# Create your models here.

class Crop_info(models.Model):
    farmer = models.CharField(max_length = 20)
    crop_name = models.CharField(max_length = 20)
    crop_species = models.CharField(max_length = 20)
    # geolocation_lat = models.DecimalField(max_digits = 10, decimal_places = 8) #Can use django-easy-maps package later on
    # geolocation_lon = models.DecimalField(max_digits = 10, decimal_places = 8)
    crop_age = models.IntegerField()
    crop_height = models.IntegerField()
    # timestamp
    # hash
    # p_hash
    def __str__(self):
        return self.crop_name


class Btn_display(models.Model):
    def __str__(self):
        return self
