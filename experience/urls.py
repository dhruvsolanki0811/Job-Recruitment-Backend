from django.urls import path
from . import views
urlpatterns = [
    path('',views.CreateExperienceView.as_view() , name='create-experience'),
    path('user/<str:jobseekername>',views.get_experiences_by_user , name='user-experience'),
    path('<int:pk>',views.SingleExperienceView.as_view() , name='user-experience'),
    
]
