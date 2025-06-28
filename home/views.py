from django.shortcuts import render
from django.http import HttpResponse


def htmx_demo(request):
    return HttpResponse("HTMX is working! Content loaded dynamically.")
