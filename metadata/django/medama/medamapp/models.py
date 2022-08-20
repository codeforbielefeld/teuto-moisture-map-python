import uuid
from uuid import uuid4
from django.db import models

class User(models.Model):
    user_external_id = models.UUIDField(max_length=16, default=uuid.uuid4) # UUID
    username = models.CharField(max_length=100) # PII!
    email = models.CharField(max_length=200) # PII!
    password = models.CharField(max_length=100)
    ttn_api_key = models.CharField(max_length=200)
    #ttn_username = models.CharField(max_length=100) ?

    def __str__(self):
        return str("id: " + str(self.id) + ", username: " + self.username)

class Location(models.Model):
    location_external_id = models.UUIDField(max_length=16, default=uuid.uuid4) # UUID
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.IntegerField() # m
    depth = models.IntegerField() # cm
    soil_type = models.CharField(max_length=100)

    def __str__(self):
        return str("id: " + str(self.id) + ", lat: " + str(self.latitude) + ", lon: " + str(self.longitude) + ", alt: " + str(self.altitude) + ", depth: " + str(self.depth) + ", soil: " + self.soil_type)

class Sensor(models.Model):
    device_external_id = models.UUIDField(max_length=16, default=uuid.uuid4) # UUID
    device_id = models.CharField(max_length=100)
    label = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    SENSOR_STATUS = (
        ('m', 'Maintenance'), # configured, but temp out of order due to maintenance
        ('o', 'Out-of-order'), # configured, but not working
        ('d', 'Deployed'), # configured and working
        ('n', 'New'), # not yet configured in ttn
        ('r', 'Ready'), # configured in TTN but not yet deployed
    )

    status = models.CharField(
        max_length=1,
        choices=SENSOR_STATUS,
        blank=True,
        default='n',
        help_text='Senor status',
    )

    def __str__(self):
        return str("device_id: " + str(self.device_id) + ", label: " + self.label)