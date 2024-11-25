from django.db import models
from contestant.models import Contestant
class Vote(models.Model):
    
    ip = models.GenericIPAddressField()  # IP as primary key and unique
    vote_id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)  # To store contestant's name
    voted_to = models.ForeignKey(Contestant, on_delete=models.CASCADE)  # Foreign key to Contestant
    score = models.JSONField(null=True, blank=True, default=list)
    created_on = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when a vote is created
    event_type = models.SmallIntegerField(choices=[(0, 'male 0'), (1, 'girl 1'), (2, 'performance 2'), (3, 'boang 3')], default=0)

    def __str__(self):
        return str(self.vote_id)
