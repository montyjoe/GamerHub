
from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re, bcrypt, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, data):
        errors = []
        try: #check to see if the email is already in use
            User.objects.get(email=data['email'])
            print 'email is already registered'
            errors.append('This email is already registered')
        except:
            pass
            #first name validations
        if data['first_name'] == '':
            errors.append('First name cannot be blank')
        if not data['first_name'].isalpha():
            errors.append('First Name can only be characters')
        #Last Name Validations
        if data['last_name'] == '':
            errors.append('Last name cannot be blank')
        if not data['last_name'].isalpha():
            errors.append('Last name can only be characters')
        if data['gamer_tag'] == '':
            errors.append('Gamer tag cannot be blank')
        #email Validations

        if data['email'] == '':
            errors.append('The Email Field cannot be blank')
        try:
            validate_email(data['email'])
        except ValidationError:
            errors.append('Invalid Email')


        # Password validation
        if len(data['password']) < 8 :
            errors.append('Password must be at least eight characters long.')
        if data['password'] != data['confirm']:
            errors.append("Passwords do not match")


        if len(errors) == 0: #if there are no errors in the validations
            data['password'] = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())
            user = User.objects.create( # create the new user
                first_name=data['first_name'],
                last_name=data['last_name'],
                gamer_tag=data['gamer_tag'],
                email=data['email'],
                password=data['password'],
            )
            print 'User was added'
            return {'user': user, 'errors': None}
        else:
            print 'User was NOT added'
            return {'user': None, 'errors': errors}



    def login(self, data): #the function for validating a log in
        errors = []
        try:
            foundUser = User.objects.get(email=data['email'])
            if bcrypt.hashpw(data['password'].encode('utf8'), foundUser.password.encode('utf8')) == foundUser.password.encode('utf8'):
                print 'success'
            else:
                errors.append('Incorrect Login Credentials')
            # print "User is found"
            # if foundUser.password == data['password']:
            #     return {'user': foundUser, 'errors': None}
            # else:
            #     errors.append('Email or password is incorrect')
            #     return {'user': None, 'errors': errors }

        except:
            print "there is no user with that name"
            errors.append('Email or password is incorrect')
            return {'user': None, 'errors': errors }
        if len(errors) == 0:
            return {'user': foundUser, 'errors': None}
        else:
            return {'user': None, 'errors': errors}


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gamer_tag = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
