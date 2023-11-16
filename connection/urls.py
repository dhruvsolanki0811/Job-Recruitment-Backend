from django.urls import path,include
from . import views

urlpatterns = [
    path('create', views.CreateConnectionView.as_view(), name='create-connection'),
    path('accept/<int:pk>', views.AcceptConnectionView.as_view(), name='accept-connection'),
    path('reject/<int:pk>', views.RejectConnectionView.as_view(), name='reject-connection'),
    path('connections', views.AllConnectedUsersView.as_view(), name='user-connections'),
    path('block/<int:pk>', views.BlockConnectionView.as_view(), name='block-connection'),
]