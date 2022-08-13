from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100) # PII!
    email = models.CharField(max_length=200) # PII!
    password = models.CharField(max_length=100)
    ttn_api_key = models.CharField(max_length=200)
    #ttn_username = models.CharField(max_length=100) ?

    def __str__(self):
        return str("id: " + str(self.id) + ", username: " + self.username)

class Location(models.Model):
    location_id = models.CharField(max_length=16) # UUID
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.IntegerField() # m
    depth = models.IntegerField() # cm
    soil_type = models.CharField(max_length=100)

    def __str__(self):
        return str("id: " + str(self.id) + ", lat: " + str(self.latitude) + ", lon: " + str(self.longitude) + ", alt: " + str(self.altitude) + ", depth: " + str(self.depth) + ", soil: " + self.soil_type)

class Sensor(models.Model):
    device_id = models.CharField(max_length=100)
    label = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str("device_id: " + str(self.device_id) + ", label: " + self.label)