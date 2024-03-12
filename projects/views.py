from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from rest_framework import generics,status,serializers
from accounts.models import JobSeeker

class CreateProjectView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        if JobSeeker.objects.filter(user=self.request.user).exists():
            serializer.save()
        else:   
            raise serializers.ValidationError({'error': 'User is not a job seeker'})

@api_view(['GET'])
def get_projects(_, jobseekerusername):
    try:
        jobseeker=JobSeeker.objects.get(user__username=jobseekerusername)
        projects = Project.objects.filter(job_seeker=jobseeker)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    except JobSeeker.DoesNotExist:
        return Response({"error": "Jobseeker not found for the given job seeker ID"}, status=404)
    
class SingleProjectView(generics.RetrieveAPIView):
    serializer_class=ProjectSerializer
    queryset=Project.objects.all()

class SingleEditProjectView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=ProjectSerializer
    queryset=Project.objects.all()
    permission_classes = [IsAuthenticated]
