from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
def index(request):
    with open('main/siteInformation.json') as json_file:
        site_info = json.load(json_file)
    return render(request, "index.html", {'site_info': site_info})