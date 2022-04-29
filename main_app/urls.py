from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.JobList.as_view(), name='jobs_index'),
    path('jobs/<int:pk>/', views.JobDetail.as_view(), name='jobs_detail'),
    path('jobs/create/', views.JobCreate.as_view(), name='jobs_create'),
    path('jobs/<int:pk>/update/', views.JobUpdate.as_view(), name='jobs_update'),
]