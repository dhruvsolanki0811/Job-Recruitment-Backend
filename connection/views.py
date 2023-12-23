from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, status,serializers
from rest_framework.permissions import IsAuthenticated
from .models import Connection, JobSeeker
from .serializers import ConnectionSerializer
from rest_framework.response import Response
from accounts.serializers import JobSeekerSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User

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
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_connection(request, user_id):

    # Check if the specified user ID exists
    try:
        target_user_id = user_id
        current_user=JobSeeker.objects.get(user=request.user.id)
    except JobSeeker.DoesNotExist:
        return Response({'error': 'Not a authorized user requesting'}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if there is a connection between the two users
    connection = Connection.objects.filter(user1=current_user.id, user2=target_user_id)
    if not connection.exists():
        connection=Connection.objects.filter(user2=current_user.id, user1=target_user_id)
    connection=connection.first()
    if not connection:
        return Response({'error': 'Connection not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the current user is authorized to delete the connection
    if current_user != connection.user1 and current_user != connection.user2:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    # Delete the connection
    connection.delete()

    return Response({'message': 'Connection deleted successfully'}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def accept_connection(request, user1_id):
    user2 = request.user
    try:
        srcUser=User.objects.get(id=user2.id)
        print(srcUser)
        user2=JobSeeker.objects.get(user=srcUser.id)
        print(user2)
        
        user1_id=JobSeeker.objects.get(id=user1_id)
        print(user1_id)

    except JobSeeker.DoesNotExist:
        return Response({'error': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        print(user1_id,user2)
        connection = Connection.objects.get( user1=user1_id.id, user2=user2.id, status=Connection.PENDING)
    except Connection.DoesNotExist:
        return Response({'error': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)

    connection.status = Connection.ACCEPTED
    connection.save()

    return Response({'message': 'Connection request accepted.'}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def reject_connection(request, user1_id):
    user2=request.user
    try:
        srcUser=User.objects.get(id=user2.id)
        print(srcUser)
        user2=JobSeeker.objects.get(user=srcUser.id)
        
        user1_id=JobSeeker.objects.get(id=user1_id)
        print(user1_id)

    except JobSeeker.DoesNotExist:
        return Response({'error': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)


    except JobSeeker.DoesNotExist:
        return Response({'error': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        print(user1_id,user2)
        connection = Connection.objects.get( user1_id=user1_id.id, user2=user2.id, status=Connection.PENDING)
    except Connection.DoesNotExist:
        return Response({'error': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)

    connection.status = Connection.REJECTED
    connection.rejected_by = user2
    connection.save()

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
    
        return Response({'message': 'Connection blocked.'}, status=status.HTTP_200_OK)\
            
    
class ListPendingConnectionRequestsSentView(generics.ListAPIView):
    serializer_class = JobSeekerSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if not JobSeeker.objects.filter(user=user).exists():  
            raise ValidationError({'error': 'Unauthorized'},401)
        jobseeker = self.request.user.jobseeker
        pendingRequest =Connection.objects.filter(user1=jobseeker, status=Connection.PENDING)
        seekerList=[]
        for conn in pendingRequest:
            print((conn.user2))
            seekerList.append(conn.user2)
        return seekerList 

class ListPendingConnectionRequestsReceivedView(generics.ListAPIView):
    serializer_class = JobSeekerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not JobSeeker.objects.filter(user=user).exists():  
            raise ValidationError({'error': 'Unauthorized'},401)
        jobseeker = self.request.user.jobseeker
        connectionReceived=Connection.objects.filter(user2=jobseeker, status=Connection.PENDING)
        seekerList=[]
        for conn in connectionReceived:
            seekerList.append(conn.user1)
        return seekerList


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_connection_status(request, user_id):

    # Check if the specified user ID exists
    try:
        target=User.objects.filter(username=user_id)[0]
        
    except:
        return Response({'error': 'User not found'}, status=404)

    try:
        target_user = JobSeeker.objects.get(user=target.id)
        user=JobSeeker.objects.get(user=request.user.id)
    except JobSeeker.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    print(target_user,request.user)
    # Check if there is a connection request or accepted connection betwe
    # en the two users
    print(Connection.objects.filter(user2=user.id, user1=target_user.id))
    connection = Connection.objects.filter(user2=user.id, user1=target_user.id)
    print(connection,'//////////////////////////')
    if connection.exists():
        connection_status = connection[0].status
    else:
        connection_status=None
    print(connection,connection_status,"!")
    if connection_status is None:
        connection = Connection.objects.filter(user1=user, user2=target_user)

        # connection_status = connection.status if connection else None
        if connection.exists():
            connection_status = connection[0].status
        else:
            connection_status=None
            
        if connection is not None and connection_status ==Connection.PENDING:
            connection_status="Requested"
            
            
        
    response_data = {
        'connection_status': connection_status,
        }
    print(response_data)
    return Response(response_data, status=200)
   
