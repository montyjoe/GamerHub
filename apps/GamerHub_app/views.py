from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, HttpResponse,redirect
from .models import User, Profile, GameList, ProPicture
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta
import math
from . import services
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
    new_games = []
    for game in gamelist:
        if game.picture_path[:4] == '&url=':
            game.picture_path = game.picture_path[5:]
            new_games.append(game)
        else:
            new_games.append(game)
        print game.picture_path
    length = len(new_games)
    context = {
        'user': user_profile,
        'profile': profile,
        'gamelist': new_games,
        'length' : length,
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

def search(request):
    search = request.GET.get('search-info')
    result = services.search_database(search)
    return JsonResponse(result, safe=False)

def addGame(request, id, name):
    data = {
    'name': name,
    'game_id': id,
    'user_id': request.session['user']
    }
    GameList.add_game(data)
    return redirect('/')
    # result = {"added": True}
    # return JsonResponse(result, safe=False)

def deleteGame(request, id):
    delete_me = GameList.objects.get(id=id)
    delete_me.delete()
    return redirect("/profile")

def searchGame(request):
    print("true")
    headers={'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': '2w5qsci3na5nzblfr60mcgju4g9zi9'}
    game = 'https://api.twitch.tv/kraken/search/games?query='+request.POST['game']
    r = requests.get(game, headers=headers)
    json_data = r.json()
    print(json_data)
    results = json_data['games']
    gameArr = []
    for game in results:
        game_json = {}
        game_json['id'] = game['giantbomb_id']
        game_json['label'] = game['name']
        game_json['cover'] = game['box']['large']
        gameArr.append(game_json)
    data = {
        'gameInfo':gameArr
    }
    return render(request, 'GamerHub_app/search.html', data)




# {u'games': [{u'box': {u'large': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%202-272x380.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%202-52x72.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%202-136x190.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%202-{width}x{height}.jpg'}, u'giantbomb_id': 52647, u'name': u'Destiny 2', u'localized_name': u'Destiny 2', u'locale': u'', u'popularity': 19235, u'logo': {u'large': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%202-240x144.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%202-60x36.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%202-120x72.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%202-{width}x{height}.jpg'}, u'_id': 497057}, {u'box': {u'large': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny-272x380.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny-52x72.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny-136x190.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny-{width}x{height}.jpg'}, u'giantbomb_id': 36067, u'name': u'Destiny', u'localized_name': u'Destiny', u'locale': u'', u'popularity': 131, u'logo': {u'large': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny-240x144.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny-60x36.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny-120x72.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny-{width}x{height}.jpg'}, u'_id': 280721}, {u'box': {u'large': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20Child-272x380.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20Child-52x72.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20Child-136x190.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20Child-{width}x{height}.jpg'}, u'giantbomb_id': 55796, u'name': u'Destiny Child', u'localized_name': u'Destiny Child', u'locale': u'', u'popularity': 1, u'logo': {u'large': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20Child-240x144.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20Child-60x36.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20Child-120x72.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20Child-{width}x{height}.jpg'}, u'_id': 493615}, {u'box': {u'large': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20Spirits-272x380.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20Spirits-52x72.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20Spirits-136x190.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20Spirits-{width}x{height}.jpg'}, u'giantbomb_id': 42893, u'name': u'Destiny of Spirits', u'localized_name': u'Destiny of Spirits', u'locale': u'', u'popularity': 0, u'logo': {u'large': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20Spirits-240x144.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20Spirits-60x36.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20Spirits-120x72.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20Spirits-{width}x{height}.jpg'}, u'_id': 369558}, {u'box': {u'large': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20Ancient%20Kingdoms-272x380.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20Ancient%20Kingdoms-52x72.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20Ancient%20Kingdoms-136x190.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20Ancient%20Kingdoms-{width}x{height}.jpg'}, u'giantbomb_id': 55391, u'name': u'Destiny of Ancient Kingdoms', u'localized_name': u'Destiny of Ancient Kingdoms', u'locale': u'', u'popularity': 0, u'logo': {u'large': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20Ancient%20Kingdoms-240x144.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20Ancient%20Kingdoms-60x36.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20Ancient%20Kingdoms-120x72.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20Ancient%20Kingdoms-{width}x{height}.jpg'}, u'_id': 494121}, {u'box': {u'large': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20the%20Doctors-272x380.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20the%20Doctors-52x72.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20the%20Doctors-136x190.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20the%20Doctors-{width}x{height}.jpg'}, u'giantbomb_id': 21932, u'name': u'Destiny of the Doctors', u'localized_name': u'Destiny of the Doctors', u'locale': u'', u'popularity': 0, u'logo': {u'large': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20the%20Doctors-240x144.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20the%20Doctors-60x36.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20the%20Doctors-120x72.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20the%20Doctors-{width}x{height}.jpg'}, u'_id': 19949}, {u'box': {u'large': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20an%20Emperor-272x380.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20an%20Emperor-52x72.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20an%20Emperor-136x190.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20of%20an%20Emperor-{width}x{height}.jpg'}, u'giantbomb_id': 1624, u'name': u'Destiny of an Emperor', u'localized_name': u'Destiny of an Emperor', u'locale': u'', u'popularity': 0, u'logo': {u'large': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20an%20Emperor-240x144.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20an%20Emperor-60x36.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20an%20Emperor-120x72.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20of%20an%20Emperor-{width}x{height}.jpg'}, u'_id': 1482}, {u'box': {u'large': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20Architect-272x380.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20Architect-52x72.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20Architect-136x190.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20Architect-{width}x{height}.jpg'}, u'giantbomb_id': 14927, u'name': u'Destiny Architect', u'localized_name': u'Destiny Architect', u'locale': u'', u'popularity': 0, u'logo': {u'large': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20Architect-240x144.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20Architect-60x36.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20Architect-120x72.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20Architect-{width}x{height}.jpg'}, u'_id': 13694}, {u'box': {u'large': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20Links-272x380.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20Links-52x72.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20Links-136x190.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-boxart/Destiny%20Links-{width}x{height}.jpg'}, u'giantbomb_id': 24225, u'name': u'Destiny Links', u'localized_name': u'Destiny Links', u'locale': u'', u'popularity': 0, u'logo': {u'large': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20Links-240x144.jpg', u'small': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20Links-60x36.jpg', u'medium': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20Links-120x72.jpg', u'template': u'https://static-cdn.jtvnw.net/ttv-logoart/Destiny%20Links-{width}x{height}.jpg'}, u'_id': 21940}]}





# end
