from __future__ import unicode_literals

from django.shortcuts import render

def index(request):
    return render(request, 'GamerHub_app/index.html')
# Create your views here.
