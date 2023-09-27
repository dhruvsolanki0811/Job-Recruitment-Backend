from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('',views.hello_world,name="hi"),
    path('organization/login',views.organizationlogin,name='organization-login'),
    path('jobseeker/login',views.jobseekerlogin,name='jobseeker-login'),

    path('create/organization',views.CreateOrganizationListView.as_view(),name='create-organization'),
    path('organization/<str:username>',views.OrganizationView.as_view(),name='organization-detail'),
    path('<int:pk>/organization',views.OrganizationIdView.as_view(),name='organizationid-detail'),

    path('create/jobseeker',views.CreateJobSeekerListView.as_view(),name='create-jobseeker'),
    path('jobseeker/<str:username>',views.JobSeekerView.as_view(),name='jobseeker-detail'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]