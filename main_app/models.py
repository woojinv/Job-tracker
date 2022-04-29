from django.db import models
from django.urls import reverse

# Create your models here.
class Job(models.Model):
    company = models.CharField(max_length=100)
    title = models.CharField('Job Title', max_length=100)
    salary = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date_applied = models.DateField('Date Applied')
    tech_reqs = models.TextField('Technical Requirements', max_length=500)
    status = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    description = models.TextField(max_length=250)

    def __str__(self):
        return f"{self.company}"
    
    def get_absolute_url(self):
        return reverse('jobs_detail', kwargs={'pk': self.id})