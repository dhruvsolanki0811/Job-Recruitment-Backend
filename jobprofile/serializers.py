from rest_framework import serializers
from accounts.serializers import OrganizationSerializer
from .models import JobProfile
from accounts.models import Organization
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

class JobProfileSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name',read_only=True)
    organization_id= serializers.CharField(source='organization.id',write_only=True)
    organization_profile_pic= serializers.CharField(source='organization.profile_pic',read_only=True)

    # organization=OrganizationSerializer()
    class Meta:
        model=JobProfile
        fields=['id','organization_id','organization_name','organization_profile_pic','role','skills_required','required_experience','employee_type','salary','job_description','created_at']
        extra_kwargs = {
            'id':{'read_only':True}
            
        }
        
    def create(self, validated_data):
        user= self._context['request'].user
        data=validated_data
        print(data)
        
        if not Organization.objects.filter(pk=data['organization']['id']).exists():
            raise serializers.ValidationError({'error': 'No such organizations exists!'})
        organization=Organization.objects.filter(pk=data['organization']['id']).first()
        
        if not organization.user.username== user.username:
            raise PermissionDenied({'error': 'You are not the owner of organization!'})            
        
        jobProfile=JobProfile(role=data['role'],required_experience=data['required_experience'],
                              employee_type=data['employee_type'],salary=data['salary'],
                              job_description=data['job_description'],organization=organization,
                              skills_required=data['skills_required'])
        jobProfile.save()
        return jobProfile