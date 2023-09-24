from django.db import models
from accounts.models import Organization
# Create your models here.
class JobProfile(models.Model):
    role=models.CharField(max_length=100)

    required_experience=models.IntegerField()
    employee_type=models.CharField(max_length=100)
    salary=models.IntegerField()
    job_description=models.TextField()
    
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.role   
    
    class Meta:
        ordering = ('-created_at', )

