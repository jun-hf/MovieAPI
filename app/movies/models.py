from django.contrib.auth.models import AbstractUser
from django.db import models 

# Create your models here.

class CustomUser(AbstractUser):
    pass 


class Movie(models.Model):
    title = models.CharField(max_length=225)
    genre = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"