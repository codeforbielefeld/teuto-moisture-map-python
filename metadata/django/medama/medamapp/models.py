from tkinter.ttk import Treeview
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100) # PII!
    email = models.CharField(max_length=200) # PII!
    password = models.CharField(max_length=100)
    ttn_api_key = models.CharField(max_length=200)
    #ttn_username = models.CharField(max_length=100) ?

class Location(models.Model):
    location_id = models.CharField(max_length=16) # UUID
    latitude = models.FloatField
    longitude = models.FloatField
    altitude = models.IntegerField # m
    depth = models.IntegerField # cm
    soil_type = models.CharField(max_length=100)

class Sensor(models.Model):
    device_id = models.CharField(max_length=100)
    label = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)