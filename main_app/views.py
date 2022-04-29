from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .models import Job

def home(request):
    return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')

# def jobs_index(request):
#     jobs = Job.objects.all()
#     return render(request, 'jobs/index.html', {'jobs': jobs})

class JobList(ListView):
    model = Job

class JobDetail(DetailView):
    model = Job

class JobCreate(CreateView):
    model = Job
    fields = '__all__'

class JobUpdate(UpdateView):
    model = Job
    fields = '__all__'