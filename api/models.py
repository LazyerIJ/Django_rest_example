from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=15)
    nickname = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
