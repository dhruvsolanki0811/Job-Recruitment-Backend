from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import generics
from .serializers import UserSerializer,OrganizationSerializer,JobSeekerSerializer
from django.contrib.auth.models import User
from .models import Organization,JobSeeker
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .permissions import isOrganizationPermissionOrReadOnly
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
@api_view(['GET'])
# @authentication_classes([])
@permission_classes([isOrganizationPermissionOrReadOnly])
def hello_world(request):
    return Response({"message": "Hello, world!"})


class CreateOrganizationListView(generics.ListCreateAPIView):
    serializer_class=OrganizationSerializer
    queryset=Organization.objects.all()
    

class OrganizationView(generics.RetrieveDestroyAPIView):
    serializer_class=OrganizationSerializer
    queryset=Organization.objects.all()
    # permission_classes=[isOrganizationPermission]
    def get_object(self):
        username = self.kwargs['username']
        try:
            user = User.objects.get(username=username)
            organization = self.queryset.filter(user=user)
            if not organization.exists() :
                raise ValidationError({"detail": f"Organization with name '{username}' not found."})
            return organization.first()
        except User.DoesNotExist :
            raise ValidationError({"detail": f"Organization with name '{username}' not found."})
    def perform_destroy(self, instance):
        # Delete the User instance associated with the Organization
        instance.user.delete()
        # Delete the Organization instance
        instance.delete()
        
class OrganizationIdView(generics.RetrieveDestroyAPIView):
    queryset=Organization.objects.all()
    serializer_class=OrganizationSerializer

    def perform_destroy(self, instance):
        # Delete the User instance associated with the Organization
        instance.user.delete()
        # Delete the Organization instance
        instance.delete()




    # def retrieve(self, request, username, *args, **kwargs):
        
    #     user= User.objects.filter(username=username)
    #     if not user.exists():
    #         return Response({"detail": f"Organization with username '{username}' not found."}, status=status.HTTP_404_NOT_FOUND)
            
    #     organization = self.queryset().filter(user=user[0].id)
    #     if not organization.exists() :
    #         return Response({"detail": f"Organization with username '{username}' not found."}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = self.serializer_class(organization[0])
    #     return Response(serializer.data)
            # return Response({"detail": f"Organization with username '{username}' not found."}, status=status.HTTP_404_NOT_FOUND)


class CreateJobSeekerListView(generics.ListCreateAPIView):
    serializer_class=JobSeekerSerializer
    queryset=JobSeeker.objects.all()
    
class JobSeekerView(generics.RetrieveDestroyAPIView):
    serializer_class=JobSeekerSerializer
    queryset=JobSeeker.objects.all()
    
    def get_object(self):
        username = self.kwargs['username']
        try:
            user = User.objects.get(username=username)
            jobseeker = self.queryset.filter(user=user)
            if not jobseeker.exists() :
                raise ValidationError({"detail": f"Jobseeker with username '{username}' not found."})
            return jobseeker.first()
        except User.DoesNotExist :
            raise ValidationError({"detail": f"Jobseeker with username '{username}' not found."})
    def perform_destroy(self, instance):
        # Delete the User instance associated with the Organization
        instance.user.delete()
        # Delete the Organization instance
        instance.delete()

@api_view(['POST'])
def organizationlogin(request):
    email = request.data.get('email', None)
    password = request.data.get('password', None)

    if not email or not password:
        return Response({'error': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        organization=Organization.objects.get(user=user)
    except Organization.DoesNotExist:
        return Response({'error': 'Invalid email and password.'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

    org_resp=OrganizationSerializer(organization)
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)


    return Response({"refresh":str(refresh),'access': access_token,"role":"Organization","user":org_resp.data}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def jobseekerlogin(request):
    email = request.data.get('email', None)
    password = request.data.get('password', None)

    if not email or not password:
        return Response({'error': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        jobseeker=JobSeeker.objects.get(user=user)
    except JobSeeker.DoesNotExist:
        return Response({'error': 'Invalid email and password.'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

    jobseeker_resp=JobSeekerSerializer(jobseeker)
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)


    return Response({"refresh":str(refresh),'access': access_token,"role":"Jobseeker","user":jobseeker_resp.data}, status=status.HTTP_200_OK)
    
    
    
    