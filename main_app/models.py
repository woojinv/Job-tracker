from django.db import models

# Create your models here.
class Job(models.Model):
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    salary = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date_applied = models.DateField('date applied')
    tech_reqs = models.TextField(max_length=500)
    status = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    description = models.TextField(max_length=250)

    def __str__(self):
        return f"{self.company}"