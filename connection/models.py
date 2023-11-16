from django.db import models
from accounts.models import JobSeeker
# Create your models here.
class Connection(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    BLOCKED = 'blocked'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (BLOCKED, 'Blocked'),
    ]
    
    user1 = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name="connections_from")
    user2 = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name="connections_to")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    established_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Connection between {self.user1.user.username} and {self.user2.user.username}, Status: {self.status}"