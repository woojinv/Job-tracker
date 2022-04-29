from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .models import Job

def home(request):
    return render(request, 'home.html')

class JobList(ListView):
    model = Job

class JobDetail(DetailView):
    model = Job

class JobCreate(CreateView):
    model = Job
    fields = ['company', 'title', 'salary', 'location', 'date_applied', 'tech_reqs', 'status', 'source', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class JobUpdate(UpdateView):
    model = Job
    fields = '__all__'

class JobDelete(DeleteView):
    model = Job
    success_url = '/jobs/'