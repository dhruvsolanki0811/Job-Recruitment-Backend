from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import Application
from .serializers import ApplicationSerializer
from rest_framework.response import Response
from rest_framework import status
from accounts.models import JobSeeker
from accounts.serializers import JobSeekerSerializer
from jobprofile.models import JobProfile
from jobprofile.serializers import JobProfileSerializer
class CreateApplicationListView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    

@api_view(['GET'])
def getApplicationView(request,id):
    try:
        application=Application.objects.get(pk=id)
    except Application.DoesNotExist:
        return Response({'error': 'No Such application with that primary key.'}, status=status.HTTP_404_NOT_FOUND)
    try:
        jp=JobProfile.objects.get(pk=application.job_profile.id)
    except JobProfile.DoesNotExist:
        return Response({'error': 'Some error.'}, status=status.HTTP_404_NOT_FOUND)
    
    try: 
        js=JobSeeker.objects.get(pk=application.job_seeker.id)
    except JobSeeker.DoesNotExist:
        return Response({'error': 'Some error.'}, status=status.HTTP_404_NOT_FOUND)

    jp_resp=JobProfileSerializer(jp)
    js_resp=JobSeekerSerializer(js)
    print(js_resp)
    
    print(jp_resp)
    
    resp={"id":application.id,"status":application.status,"jobseeker":js_resp.data,"jobprofile":jp_resp.data}    
    
    
    return Response(resp,status=status.HTTP_200_OK)
    
    
    