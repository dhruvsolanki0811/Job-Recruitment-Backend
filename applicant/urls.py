from django.urls import path
from . import views

urlpatterns = [
    path('application',views.CreateApplicationListView.as_view() , name='create-jobprofile'),
    path('application/<int:id>',views.getApplicationView,name="getapplication"),
    path('job_applications/<int:job_profile_id>', views.job_applications, name='job_applications'),
    path('user_applied_jobs/<str:username>', views.user_applied_jobs, name='user_applied_jobs'),
    path('status/<int:job_profile_id>', views.has_applied_to_job, name='user_has_applied_jobs'),

]
