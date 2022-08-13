from django.contrib import admin

from .models import Location, User, Sensor

admin.site.register(Location)
admin.site.register(User)
admin.site.register(Sensor)
