# appointments/models.py

from django.contrib.auth.models import User
from django.db import models

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    status = models.CharField(max_length=20, default='Booked')  # New field

    def __str__(self):
        return f"{self.user.username} - {self.date} at {self.time}"
