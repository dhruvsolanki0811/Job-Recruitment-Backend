from .models import Experience
from rest_framework import serializers

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['company','id', 'role', 'description', 'start_month', 'start_year', 'end_month', 'end_year','job_seeker']