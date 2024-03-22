from django.shortcuts import render
from django.http import HttpResponse


def projects(request):
    return HttpResponse("projects - Test function")

def project(request, pk):
    return HttpResponse(f"project - single, {pk}")
    