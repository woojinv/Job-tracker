from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from .models import Job, Document
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
import uuid
import boto3
import botocore
import clearbit
import os

# Add these "constant" variables below the imports
S3_BASE_URL = settings.S3_BASE_URL
BUCKET = settings.BUCKET_NAME


def home(request):
    return render(request, 'home.html')


class JobList(LoginRequiredMixin, ListView):
    model = Job

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)


@login_required
def jobs_detail(request, job_id):
    job = Job.objects.get(id=job_id)
    # clearbit.key = settings.API_KEY
    clearbit.key = os.environ['API_KEY']
    company = clearbit.Company.find(domain=f'{job.company}.com',stream=True)

    return render(request, 'main_app/job_detail.html', {
        'job': job,
        'domain': company['domain'],
        'sub_industry': company['category']['subIndustry'],
        'description': company['description'],
        'linkedin_handle': company['linkedin']['handle'],
        'twitter_handle': company['twitter']['handle'],
        'facebook_handle': company['facebook']['handle'],
    })

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


def add_document(request, job_id):
    # photo-file will be the "name" attribute on the <input type="file">
    document_file = request.FILES.get('document-file', None)
    if document_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + document_file.name[document_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(document_file, BUCKET, key, ExtraArgs={'ContentType': "application/pdf"})
            name = request._post['name']
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Document.objects.create(url=url, job_id=job_id, name=name)
        except botocore.exceptions.ClientError as err:
            print(err)
            # print('An error occurred uploading file to S3')
    return redirect('jobs_detail', job_id=job_id)
