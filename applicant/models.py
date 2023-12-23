from django.db import models

# Create your models here.
from accounts.models import JobSeeker
from jobprofile.models import JobProfile

class Application(models.Model):
    job_profile = models.ForeignKey(JobProfile, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    application_date = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
