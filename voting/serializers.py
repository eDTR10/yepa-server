from rest_framework import serializers
from .models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

    def validate(self, data):
        """
        Validate voting rules:
        - Allow one vote per IP per contestant for `event_type=2`.
        - Restrict one vote per IP for all other event types.
        """
        ip = data.get('ip')
        event_type = data.get('event_type')
        voted_to = data.get('voted_to')

        # For event_type=2, allow multiple votes from the same IP as long as it's for different contestants
        if event_type == 2:
            if Vote.objects.filter(ip=ip, event_type=event_type, voted_to=voted_to).exists():
                raise serializers.ValidationError(
                    f"IP {ip} has already voted for contestant {voted_to} in event type {event_type}."
                )
        else:
            # For all other event types, restrict one vote per IP
            if Vote.objects.filter(ip=ip, event_type=event_type).exists():
                raise serializers.ValidationError(
                    f"IP {ip} has already voted in event type {event_type}."
                )

        return data
