from .models import Experience
from .serializers import ExperienceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,serializers
from accounts.models import JobSeeker
from rest_framework.decorators import api_view
from rest_framework.response import Response

class CreateExperienceView(generics.CreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if JobSeeker.objects.filter(user=self.request.user).exists():
            serializer.save()
        else:   
            raise serializers.ValidationError({'error': 'User is not a job seeker'})


@api_view(['GET'])
def get_experiences_by_user(request, jobseekerid):
    try:
        experience = Experience.objects.filter(job_seeker_id=jobseekerid)
        serializer = ExperienceSerializer(experience, many=True)
        return Response(serializer.data)
    except Experience.DoesNotExist:
        return Response({"error": "Experience not found for the given job seeker ID"}, status=404)

class SingleExperienceView(generics.DestroyAPIView,generics.UpdateAPIView):
    serializer_class=ExperienceSerializer
    queryset=Experience.objects.all()
    authentication_classes=IsAuthenticated
