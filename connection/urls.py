from django.urls import path,include
from . import views

urlpatterns = [
    path('create', views.CreateConnectionView.as_view(), name='create-connection'),
    path('accept/<int:user1_id>', views.accept_connection, name='accept-connection'),
    path('reject/<int:user1_id>', views.reject_connection, name='reject-connection'),
    path('connections', views.AllConnectedUsersView.as_view(), name='user-connections'),
    path('block/<int:pk>', views.BlockConnectionView.as_view(), name='block-connection'),
    path('pending', views.ListPendingConnectionRequestsSentView.as_view(), name='user-connections-pendings'),
    path('received', views.ListPendingConnectionRequestsReceivedView.as_view(), name='user-connections-receieved'),
    path('status/<str:user_id>', views.get_connection_status, name='connection-status'),
    path('delete/<int:user_id>', views.delete_connection, name='delete-connection'),


]