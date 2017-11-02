# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, HttpResponse,redirect
from .models import User, Profile, GameList, ProPicture
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta
import math
from django.http import JsonResponse
import json
import requests


def profileFormat(user): # <--- this function will return profile info how we want
    first = user.first_name
    last = user.last_name
    tag = user.gamer_tag
    try :
        pic = ProPicture.objects.get(user_id=user.id)
        profile_pic = pic.picture
        is_pic = True

    except:
        profile_pic = tag[0]
        is_pic = False
    data = {
        'profile_id': user.id,
        'first_name': first,
        'gamer_tag': tag,
        'last_name': last,
        'is_profile_pic': is_pic,
        'pic_name': profile_pic
    }
    return data


def index(request):
    if "user" not in request.session:
        return redirect('/login')
    users = User.objects.filter(id = request.session['user'])
    context = {
        'users': users
    }
    return render(request, 'GamerHub_app/index.html', context)

def profile(request):
    if "user" not in request.session:
        return redirect('/login')
    users = User.objects.get(id = request.session['user'])
    profile = Profile.objects.filter(user_id = User.objects.get(id = request.session['user']))
    user_profile = profileFormat(users)
    gamelist = GameList.objects.filter(user_id=request.session["user"])
    context = {
        'user': user_profile,
        'profile': profile,
        'gamelist': gamelist
    }
    return render(request, 'GamerHub_app/profile.html', context)

def newProfilePicture(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        profilePic = ProPicture.objects.create(
        picture = uploaded_file_url,
        user_id = User.objects.get(id = request.session['user'])
        )
        profilePic.save()
        return redirect('/profile')

def editProfilePicture(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        oldProfilePic = ProPicture.objects.get(user_id = User.objects.get(id = request.session['user']))
        oldProfilePic.picture = uploaded_file_url
        oldProfilePic.save()
        return redirect('/profile')

def createProfile(request):
    if request.method == 'POST':
        profile = Profile.objects.create(
            platform1 = request.POST['platform1'],
            platform2 = request.POST['platform2'],
            platform3 = request.POST['platform3'],
            ava1 = request.POST['ava1'],
            ava2 = request.POST['ava2'],
            ava3 = request.POST['ava3'],
            gamer_type = request.POST['gamer_type'],
            user_id = User.objects.get(id = request.session['user']),
        )
        profile.save()
        return redirect('/profile')

def editProfile(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user_id = User.objects.get(id = request.session['user']))
        platform1 = request.POST['platform1']
        platform2 = request.POST['platform2']
        platform3 = request.POST['platform3']
        ava1 = request.POST['ava1']
        ava2 = request.POST['ava2']
        ava3 = request.POST['ava3']
        gamer_type = request.POST['gamer_type']
        profile.platform1 = platform1
        profile.platform2 = platform2
        profile.platform3 = platform3
        profile.ava1 = ava1
        profile.ava2 = ava2
        profile.ava3 = ava3
        profile.gamer_type = gamer_type
        profile.save()
        return redirect('/profile')

def login_page(request): #renders the login page template
    return render(request, 'GamerHub_app/login.html')

def register_page(request): #renders the register page template
    return render(request, 'GamerHub_app/register.html')

def logout(request):
    request.session.clear()
    return redirect('/login')
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
