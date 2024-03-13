from django.shortcuts import render
from rest_framework import generics
from .models import JobProfile
from .serializers import JobProfileSerializer
# from .permissions import 
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import isOrganizationPermissionOrReadOnly
from accounts.models import Organization,JobSeeker
from rest_framework.response import Response
from applicant.models import Application

from rest_framework import status

# Create your views here.
class CreateJobProfileListView(generics.ListCreateAPIView):
    serializer_class=JobProfileSerializer
    queryset=JobProfile.objects.all()
    permission_classes=[isOrganizationPermissionOrReadOnly]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields ={
        'role': ['exact','iexact','contains','istartswith','icontains'],
        'required_experience': ['exact', 'lte', 'gte'],
        'employee_type': ['exact','iexact'],
        'salary': ['exact', 'lte', 'gte'],
        'organization__name': ['exact','iexact'],
        'organization__user__username': ['exact','iexact'],  # Filter for the nested field 'name' in 'organization'
    }
    search_fields=['role','employee_type','organization__name','job_description',"organization__user__username"]
    ordering_fields = ['salary']
    def get_queryset(self):
        queryset = JobProfile.objects.all()

        # Assuming the authenticated user is available in the request
        user = self.request.user
        if user.is_authenticated:
            jobSeeker=JobSeeker.objects.filter(user=user)

            if jobSeeker.exists():
            # Exclude jobs that the authenticated user has already applied for
                applied_jobs = Application.objects.filter(job_seeker=jobSeeker[0])
                # .applications.values_list('job_profile', flat=True)
                for applied in applied_jobs:
                    queryset = queryset.exclude(id=applied.job_profile.id)
            else:
                queryset=JobProfile.objects.all()      
        return queryset
class JobProfileView(generics.RetrieveDestroyAPIView):
    serializer_class=JobProfileSerializer
    queryset=JobProfile.objects.all()
    
    
class JobProfileDeleteView(generics.DestroyAPIView):
    serializer_class=JobProfileSerializer
    queryset=JobProfile.objects.all()
    permission_classes=[IsAuthenticated]
    
