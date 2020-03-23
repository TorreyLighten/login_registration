from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def reg_val(self, postData):
        errors = {}

        if len(postData['first_name']) == 0:
            errors['first_name'] = "First name is required."
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters in length."
        elif not postData['first_name'].isalpha():
            errors['first_name'] = "First name can only contain letters."
        if len(postData['last_name']) == 0:
            errors['last_name'] = "Last name is required."
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters in length."
        elif not postData['last_name'].isalpha():
            errors['last_name'] = "Last name can only contain letters."

        users = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Email address is required."
        elif EMAIL_REGEX.match(postData['email']) == False:
            errors['email'] = "Invalid email address"
        elif len(users) > 0:
            errors['email'] = "A user with that email address already exists. If that's you, please try and log in."
        if len(postData['password']) == 0:
            errors['password'] = "Password is required"
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters in length."
        elif postData['password'] != postData['confirm_pw']:
            errors['password'] = "Passwords do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
