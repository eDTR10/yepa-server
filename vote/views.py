from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vote
from ..voting.serializers import VoteSerializer
from collections import Counter
from collections import defaultdict
class VoteCRUDView(APIView):
    authentication_classes = []  # No authentication
    permission_classes = []  # No permissions

    def get(self, request):
        """
        Retrieve votes, count `voted_to` for `event_type=1`,
        and calculate total score for `event_type=2`.
        """
        # Get all votes
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)

        # Filter votes by event_type = 1
        event_type_1_votes = votes.filter(event_type=1)
        event_type_1_voted_to_counts = Counter(vote.voted_to.uid for vote in event_type_1_votes)

        # Filter votes by event_type = 2
        event_type_2_votes = votes.filter(event_type=2)
        total_scores = defaultdict(int)

        # Calculate total scores for `event_type=2`
        for vote in event_type_2_votes:
            total_scores[vote.voted_to.uid] += sum(vote.score or [])  # Sum scores for each `voted_to`

        return Response({
            "event_type_1_voted_to_counts": event_type_1_voted_to_counts,
            "event_type_2_total_scores": total_scores
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handle creating a new vote, enforcing one IP per event type.
        """
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ip):
        """
        Delete a vote by IP.
        """
        vote = get_object_or_404(Vote, ip=ip)
        vote.delete()
        return Response({"message": "Vote deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
