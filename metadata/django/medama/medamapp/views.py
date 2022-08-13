from http.client import HTTPResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world. You're at the medama app index.")

def login(request):
    return HttpResponse("Login form here.")

def user_landingpage(request):
    return HTTPResponse("This is where logged in users can see infos about their sensor(s)")

def user_register_sensor(request):
    return HTTPResponse("This is where logged in users can add more sensors")