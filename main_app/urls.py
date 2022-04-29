from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.JobList.as_view(), name='jobs_index'),
    # path('jobs/<int:job_id>/', views.jobs_detail, name='detail',)
]