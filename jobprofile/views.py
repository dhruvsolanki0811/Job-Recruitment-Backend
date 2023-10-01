from django.shortcuts import render
from rest_framework import generics
from .models import JobProfile
from .serializers import JobProfileSerializer
# from .permissions import isOrganizationPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import isOrganizationPermissionOrReadOnly

# Create your views here.
class CreateJobProfileListView(generics.ListCreateAPIView):
    serializer_class=JobProfileSerializer
    queryset=JobProfile.objects.all()
    permission_classes=[isOrganizationPermissionOrReadOnly]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields ={
        'role': ['exact'],
        'required_experience': ['exact', 'lt', 'gt'],
        'employee_type': ['exact'],
        'salary': ['exact', 'lt', 'gt'],
        'organization__name': ['exact'],  # Filter for the nested field 'name' in 'organization'
    }
    search_fields=['role','employee_type','job_description']
    ordering_fields = ['salary']

class JobProfileView(generics.RetrieveDestroyAPIView):
    serializer_class=JobProfileSerializer
    queryset=JobProfile.objects.all()
    