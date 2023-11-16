from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, status,serializers
from rest_framework.permissions import IsAuthenticated
from .models import Connection, JobSeeker
from .serializers import ConnectionSerializer
from rest_framework.response import Response
from accounts.serializers import JobSeekerSerializer

class CreateConnectionView(generics.CreateAPIView):
    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user1 = self.request.user.jobseeker
        user2= serializer.validated_data.get('user2')
        # print(user2_id)
        user2 = get_object_or_404(JobSeeker, id=user2.id)

        # Validate that the current user matches the 'user1' in the request
        if user1.id != serializer.validated_data.get('user1').id:
            raise serializers.ValidationError({'error': 'Validation error'})

        serializer.save(user1=user1, user2=user2, status='pending')
        
class AcceptConnectionView(generics.UpdateAPIView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Validate that the current user can accept the connection
        if request.user.jobseeker != instance.user2 or instance.status != Connection.PENDING:
            raise serializers.ValidationError({'error': 'Validation error'})

        instance.status = Connection.ACCEPTED
        instance.save()

        return Response({'message': 'Connection request accepted.'}, status=status.HTTP_200_OK)
    
class RejectConnectionView(generics.UpdateAPIView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Validate that the current user can reject the connection
        if request.user.jobseeker != instance.user2 :
            raise serializers.ValidationError({'error': 'Unauthorized error'},status=status.HTTP_401_UNAUTHORIZED)
        if instance.status != Connection.PENDING:
            raise serializers.ValidationError({'error': 'Validation error'})
        instance.status = Connection.REJECTED
        instance.rejected_by = request.user.jobseeker
        instance.save()

        return Response({'message': 'Connection request rejected.'}, status=status.HTTP_200_OK)
    
class AllConnectedUsersView(generics.ListAPIView):
    serializer_class = JobSeekerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.jobseeker
        connected_users = JobSeeker.objects.filter(
            connections_to__status=Connection.ACCEPTED,
            connections_to__user1=user
        ).distinct() | JobSeeker.objects.filter(
            connections_from__status=Connection.ACCEPTED,
            connections_from__user2=user
        ).distinct()

        return connected_users
    
class BlockConnectionView(generics.UpdateAPIView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Validate that the current user can block the connection
        if request.user.jobseeker != instance.user1 and request.user.jobseeker != instance.user2:
            
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        instance.status = Connection.BLOCKED
        instance.save()

        return Response({'message': 'Connection blocked.'}, status=status.HTTP_200_OK)