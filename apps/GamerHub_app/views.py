# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta
import math
from django.http import JsonResponse
import json
import requests

def index(request):
    return render(request, 'GamerHub_app/index.html')

def login_page(request): #renders the login page template
    return render(request, 'GamerHub_app/login.html')

def register_page(request): #renders the register page template
    return render(request, 'GamerHub_app/register.html')
# Create your views here.

def log_user_in(request): # this is to the log the user in
    if request.method == 'POST':
        login_info = {
            "email": request.POST['email'],
            "password": request.POST['password']
        }

        result = User.objects.login(login_info)

        if result['errors'] == None:
            request.session['email'] = result['user'].email
            request.session['name'] = result['user'].first_name
            request.session['user'] = result['user'].id
            request.session['action'] = "logged in"
            return redirect('/')
        else:
            for error in result['errors']:
                messages.add_message(request, messages.ERROR, error)
                print error
            return redirect('/login')

def register_account(request): #this function creates the account
    if request.method == 'POST':
        account_info = {
            "first_name": request.POST['first_name'],
            "last_name": request.POST['last_name'],
            "email": request.POST['email'],
            "password": request.POST['password'],
            "gamer_tag": request.POST['gamer_tag'],
            "confirm": request.POST['confirm']
        }
        result = User.objects.register(account_info)
        if result['errors']:
            for error in result['errors']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/register')
        else:
            user_id = result['user'].id
            request.session['name'] = result['user'].first_name
            request.session['user'] = user_id
            request.session['action'] = "registered"
            return redirect('/')
