from django.db import models

# Create your models here.



class Appointment(models.Model):
    name = models.CharField(max_length=122, blank=True, null=True)





