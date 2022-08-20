from http.client import HTTPResponse
from django.shortcuts import render

from .models import Sensor

def index(request):
    return HttpResponse("Hello, world. You're at the medama app index.")

def login(request):
    return HttpResponse("Login form here.")

def user_landingpage(request, user_id):
    return HTTPResponse("This is where logged in users can see infos about their sensor(s)")

def user_profile(request, user_id):
    return HTTPResponse("This is where logged in users can see infos about their sensor(s)")

# TODO: This is not immediately required. Sensors can be registered by codeforbi staff in the beginning
def user_register_sensor(request, user_id):
    return HTTPResponse("This is where logged in users can add more sensors")