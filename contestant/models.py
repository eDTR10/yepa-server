from django.db import models

# Create your models here.
class Contestant(models.Model):
    uid = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)  # To store contestant's name
    photos = models.ImageField(upload_to='photos/', null=True, blank=True)  # To store photos
    event_type = models.SmallIntegerField(default=1)  # To define event type
    def __str__(self):
        return str(self.uid)