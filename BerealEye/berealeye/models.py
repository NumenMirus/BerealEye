from django.db import models

# Create your models here.

'''
class Users(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
'''

class Tokens(models.Model):
    token = models.CharField(max_length=255)