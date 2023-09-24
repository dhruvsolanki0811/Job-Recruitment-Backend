from django.shortcuts import render
from rest_framework import generics
from .models import JobProfile
from .serializers import JobProfileSerializer
# from .permissions import isOrganizationPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class CreateJobProfileListView(generics.ListCreateAPIView):
    serializer_class=JobProfileSerializer
    queryset=JobProfile.objects.all()
    
    permission_classes=[IsAuthenticatedOrReadOnly]
    
class JobProfileView(generics.RetrieveDestroyAPIView):
    serializer_class=JobProfileSerializer
    queryset=JobProfile.objects.all()
    