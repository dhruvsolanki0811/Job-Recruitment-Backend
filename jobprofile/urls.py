from django.urls import path
from . import views

urlpatterns = [
    path('jobprofile',views.CreateJobProfileListView.as_view() , name='create-jobprofile'),
    path('jobprofile/<int:pk>',views.JobProfileView.as_view() , name='jobprofile-detail'),
    path('jobprofile/remove/<int:pk>',views.JobProfileDeleteView.as_view() , name='jobprofile-delete'),
]

