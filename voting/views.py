from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vote
from .serializers import VoteSerializer
from .models import Vote
from contestant.models import Contestant
class VoteCRUDView(APIView):
    authentication_classes = []  # No authentication
    permission_classes = []  # No permissions
    

    def get(self, request):
        """
        Get votes grouped by event type with contestant details, sorted by total votes or total score.
        """
        response_data = {}

        # Handle each event type
        for event_type in [0, 1, 2]:
            event_votes = Vote.objects.filter(event_type=event_type)
            vote_summary = {}

            # Group by contestant and calculate total votes and total score manually
            for vote in event_votes:
                contestant = vote.voted_to
                if contestant.uid not in vote_summary:
                    vote_summary[contestant.uid] = {
                        "contestant": contestant.uid,
                        "name": contestant.name,
                        "total_votes": 0,
                        "photos": contestant.photos.url if contestant.photos else None,
                        "total_score": 0,
                    }
                vote_summary[contestant.uid]["total_votes"] += 1
                if event_type == 2:
                    vote_summary[contestant.uid]["total_score"] += sum(vote.score or [])

            # Prepare results for the event type
            event_results = list(vote_summary.values())

            # Sort results
            if event_type in [0, 1]:
                event_results = sorted(event_results, key=lambda x: x["total_votes"], reverse=True)
            elif event_type == 2:
                event_results = sorted(event_results, key=lambda x: x["total_score"], reverse=True)

            # Add sorted results to the response
            if event_type == 1:
                response_data["female_ranking"] = event_results
            elif event_type == 0:
                response_data["male_ranking"] = event_results
            elif event_type == 2:
                response_data["performance_ranking"] = event_results

        return Response(response_data, status=200)
    
    def post(self, request):
        """
        Handle bulk votes.
        """
        votes_data = request.data  # Expecting a list of votes
        if not isinstance(votes_data, list):
            return Response({"error": "Data should be a list of votes."}, status=status.HTTP_400_BAD_REQUEST)

        responses = []
        for vote_data in votes_data:
            serializer = VoteSerializer(data=vote_data)
            if serializer.is_valid():
                serializer.save()
                responses.append({"vote": serializer.data, "status": "success"})
            else:
                responses.append({"errors": serializer.errors, "status": "failed"})

        return Response(responses, status=status.HTTP_200_OK)

    def delete(self, request, ip):
        """
        Delete a vote by IP.
        """
        vote = get_object_or_404(Vote, ip=ip)
        vote.delete()
        return Response({"message": "Vote deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
