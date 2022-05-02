from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from .models import Job
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
import clearbit

def home(request):

    variable_name = 'twitch'
    clearbit.key = settings.API_KEY
    print(clearbit.key)
    company = clearbit.Company.find(domain=f'{variable_name}.com',stream=True)

    return render(request, 'home.html', {
        'company': company['name'],
        'domain': company['domain'],
        'description': company['description'],
        'industry': company['category']['industry']
    })


class JobList(LoginRequiredMixin, ListView):
    model = Job

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)


@login_required
def jobs_detail(request, job_id):
    job = Job.objects.get(id=job_id)
    clearbit.key = settings.API_KEY
    company = clearbit.Company.find(domain=f'{job.company}.com',stream=True)

    return render(request, 'main_app/job_detail.html', {
        'job': job,
        'company': company['name'],
        'domain': company['domain'],
        'description': company['description'],
        'industry': company['category']['industry'] 
    })

# class JobDetail(LoginRequiredMixin, DetailView):
#     model = Job

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         clearbit.key = 'sk_d07964faa899c455e891fd4c3a1bb102'
#         company_info = clearbit.Company.find(domain='uber.com',stream=True)

#         return context, company_info


class JobCreate(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['company', 'title', 'salary', 'location', 'date_applied', 'tech_reqs', 'status', 'source', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class JobUpdate(LoginRequiredMixin, UpdateView):
    model = Job
    fields = ['company', 'title', 'salary', 'location', 'date_applied', 'tech_reqs', 'status', 'source', 'description']


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