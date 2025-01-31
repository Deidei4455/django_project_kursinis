from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.


def index(request):
    return HttpResponse("Pagrindinis autoserviso puslapis")


def paslaugos(request):
    return HttpResponse("Tai yra autoserviso teikiamų paslaugų puslapis")
