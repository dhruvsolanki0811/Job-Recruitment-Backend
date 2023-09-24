
# Create your models here.
from django.db import models

from django.contrib.auth.models import User

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=150,unique=True)
    location = models.TextField()
    website= models.URLField(max_length=150)
    overview= models.TextField()
    founded_at= models.CharField(max_length=5)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_at', )

    def __str__(self) -> str:
        return self.user.username


class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    description= models.TextField()
    phone_number= models.CharField( max_length=50)
    no_of_years_experience= models.IntegerField()
    resume=models.URLField(max_length=200)
    skills = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.user.username    
    
    class Meta:
        ordering = ('-created_at', )

    
