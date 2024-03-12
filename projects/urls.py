from django.urls import path
from . import views

urlpatterns = [ 
    path('',views.CreateProjectView.as_view() , name='create-jobprofile'),
    path('user/<str:jobseekerusername>',views.get_projects , name='get-jobprofile-user'),
    path('<int:pk>',views.SingleEditProjectView.as_view() , name='update-single-jobprofile'),
    
]

