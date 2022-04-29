from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .models import Job
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def home(request):
    return render(request, 'home.html')

class JobList(LoginRequiredMixin, ListView):
    model = Job

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

class JobDetail(PermissionRequiredMixin, DetailView):
    model = Job
    # permission_required = 'jobs.title'
    # raise_exception = False
    

    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         return Job.objects.filter(user=self.request.user)
    #     else:
    #         return Job.objects.none()

class JobCreate(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['company', 'title', 'salary', 'location', 'date_applied', 'tech_reqs', 'status', 'source', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class JobUpdate(LoginRequiredMixin, UpdateView):
    model = Job
    fields = '__all__'

class JobDelete(LoginRequiredMixin, DeleteView):
    model = Job
    success_url = '/jobs/'


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('jobs_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)