from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from .models import Application
from .serializers import ApplicationSerializer
from rest_framework.response import Response
from rest_framework import status
from accounts.models import JobSeeker,Organization
from accounts.serializers import JobSeekerSerializer
from jobprofile.models import JobProfile
from jobprofile.serializers import JobProfileSerializer
class CreateApplicationListView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes=[IsAuthenticated]
    

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
    
    resp={"id":application.id,"status":application.status,"jobseeker":js_resp.data,"jobprofile":jp_resp.data}    
    
    
    return Response(resp,status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_applications(request, job_profile_id):
    try:
        Organization.objects.get(user=request.user.id)
    except Organization.DoesNotExist:
        return Response({"  ":"Unauthorized Request"},401)
    try:
        applications = Application.objects.filter(job_profile_id=job_profile_id)
        # serializer = ApplicationSerializer(applications, many=True)
        seeker=[]
        for user in applications:
            seeker.append(user.job_seeker)
        serializer=JobSeekerSerializer((seeker),many=True)
        return Response(serializer.data)

    except Application.DoesNotExist:
        return Response({"message": "Job profile not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_applied_jobs(request, username):
    """
    Get a list of jobs applied to by the authenticated user.
    """
    try:
        authenticated_user = request.user
        requested_user = User.objects.get(username=username)

        # Check if the authenticated user is the same as the requested user
        if authenticated_user != requested_user:
            return Response({"message": "Unauthorized access"}, status=403)
        
        job_seeker = JobSeeker.objects.filter(user=requested_user).first()
        if not job_seeker:
            return Response({"message": "User is not a JobSeeker"}, status=400)
            
        applications = Application.objects.filter(job_seeker=requested_user.jobseeker)

        # Use a dictionary to track the latest application for each unique job
        latest_applications_dict = {}
        for application in applications:
            job_id = application.job_profile.id
            if job_id not in latest_applications_dict or application.application_date > latest_applications_dict[job_id].application_date:
                latest_applications_dict[job_id] = application

        # Retrieve the jobs associated with the latest applications
        latest_applications = list(latest_applications_dict.values())
        jobs = [application.job_profile for application in latest_applications]
        
        serializer = JobProfileSerializer(jobs, many=True)  # Adjust serializer as needed
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def has_applied_to_job(request, job_profile_id):
    try:
        authenticated_user = request.user
        job_seeker = JobSeeker.objects.get(user=authenticated_user)

        try:
            job_profile = JobProfile.objects.get(pk=job_profile_id)
        except JobProfile.DoesNotExist:
            return Response({"message": "Job profile not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has applied to the specified job profile
        has_applied = Application.objects.filter(job_seeker=job_seeker, job_profile=job_profile).exists()
        response_data = {"has_applied": has_applied}
        return Response(response_data, status=status.HTTP_200_OK)

    except JobSeeker.DoesNotExist:
        return Response({"message": "User is not a JobSeeker"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)