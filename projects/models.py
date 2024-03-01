from django.db import models
from accounts.models import JobSeeker
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    description = models.TextField()
    deployed_link = models.TextField(blank=True, null=True)
    tech_stack = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    job_seeker = models.ForeignKey(JobSeeker, related_name='projects', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at', )