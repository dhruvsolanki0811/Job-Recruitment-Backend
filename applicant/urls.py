from django.urls import path
from . import views

urlpatterns = [
    path('application',views.CreateApplicationListView.as_view() , name='create-jobprofile'),
    path('application/<int:id>',views.getApplicationView,name="getapplication")
]
