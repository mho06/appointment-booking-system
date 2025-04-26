from django.db import models

# Create your models here.

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"Appointment with {self.name} on {self.date}"
