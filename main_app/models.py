from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

STATUSES = (
    ('1', 'Applying'),
    ('2', 'Applied'),
    ('3', 'Interviewing'),
    ('4', 'Pending'),
    ('5', 'Position Offered'),
    ('6', 'Position Not Offered'),
    ('7', 'Offer Rejected'),
    ('8', 'Offer Accepted')
)

# Create your models here.
class Job(models.Model):
    company = models.CharField(max_length=100)
    title = models.CharField('Job Title', max_length=100)
    salary = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date_applied = models.DateField('Date Applied')
    tech_reqs = models.TextField('Technical Requirements', max_length=500)
    status = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # documents = models.ManyToManyField(Document)



    def __str__(self):
        return f"{self.company}"
    
    def get_absolute_url(self):
        return reverse('jobs_detail', kwargs={'job_id': self.id})



class Document(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def __str__(self):
        return f"document for {self.job_id} at {self.url}."  