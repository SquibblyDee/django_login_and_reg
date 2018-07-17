from __future__ import unicode_literals
from django.db import models
import re

# Create your models here.

# This class handles all of the validation for our forms on submit
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        query = Users.objects.all().values('email')
        if len(postData['input_first_name']) < 2:
            errors["input_first_name"] = "First name should be at least 2 letters"
        for char in postData['input_first_name']:
            if char.isalpha() == False:
                errors["input_first_name"] = "First name cannot contain numbers"
        if len(postData['input_last_name']) < 2:
            errors["input_last_name"] = "Last name should be at least 2 letters"
        for char in postData['input_last_name']:
            if char.isalpha() == False:
                errors["input_last_name"] = "Last name cannot contain numbers"
        if "@" not in postData['input_email']:
            errors["input_email"] = "Email needs to have an @"
        for row in query:
            for key in row:
                print("KEYYYYY", row[key])
                if row[key] == postData['input_email']:
                    errors["input_email"] = "Email is taken"
        if len(postData['input_password']) < 8:
            errors["input_password"] = "Password should be at least 8 characters"
        if postData['input_confirm_password'] != postData["input_password"]:
            errors["input_confirm_password"] = "Passwords must match"
        return errors

# This is our table
class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    # *************************
    # Connect an instance of BlogManager to our Blog model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    objects = UserManager()
    # *************************
