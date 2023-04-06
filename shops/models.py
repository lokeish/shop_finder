from django.db import models
from django.contrib.gis.db import models as gis_models

class Shop(models.Model):
    name = gis_models.CharField(max_length=100)
    location = gis_models.PointField()
    address = gis_models.CharField(max_length=1000)
    created_at = gis_models.DateTimeField(auto_now_add=True, null=True)
    updated_at = gis_models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def distance_from(self, latitude, longitude):
        point = Point(longitude, latitude)
        return self.location.distance(point) * 100  # distance in km