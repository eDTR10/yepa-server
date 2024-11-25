from rest_framework import serializers
from .models import Contestant

class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = '__all__'
