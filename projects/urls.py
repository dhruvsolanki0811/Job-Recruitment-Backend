from django.urls import path
from . import views

urlpatterns = [ 
    path('',views.CreateProjectView.as_view() , name='create-jobprofile'),
    path('user/<int:jobseekerid>',views.get_projects , name='create-jobprofile'),
    path('<int:pk>',views.SingleProjectView.as_view() , name='single-jobprofile'),
    
]

