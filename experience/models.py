from django.db import models
from accounts.models import JobSeeker
# Create your models here.
class Experience(models.Model):
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    tech_stack = models.JSONField(default=list)
    start_month = models.CharField()  
    start_year = models.PositiveSmallIntegerField()
    end_month = models.CharField(blank=True, null=True)  
    end_year = models.PositiveSmallIntegerField(blank=True, null=True)  
    job_seeker = models.ForeignKey(JobSeeker, related_name='experience', on_delete=models.CASCADE)
    def __str__(self):
        return self.role
