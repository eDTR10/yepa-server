from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Contestant
from .serializers import ContestantSerializer

class ContestantCRUDView(APIView):
    # Disable authentication and permission checks
    authentication_classes = []  # No authentication
    permission_classes = []  # No permission checks

    def get(self, request, uid=None):
        """
        Retrieve one contestant by UID or group all contestants by event type.
        """
        if uid:
            contestant = get_object_or_404(Contestant, uid=uid)
            serializer = ContestantSerializer(contestant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            contestants = Contestant.objects.all()
            grouped_data = {}

            # Group contestants by event_type
            for contestant in contestants:
                event_type = contestant.event_type
                if event_type not in grouped_data:
                    grouped_data[event_type] = []
                grouped_data[event_type].append(ContestantSerializer(contestant).data)

            # Format response to include event type labels
            formatted_response = {
                f"event_type_{event_type}": grouped_data[event_type]
                for event_type in grouped_data
            }

            return Response(formatted_response, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new contestant.
        """
        serializer = ContestantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, uid):
        """
        Update an existing contestant.
        """
        contestant = get_object_or_404(Contestant, uid=uid)
        serializer = ContestantSerializer(contestant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid):
        """
        Delete a contestant by UID.
        """
        contestant = get_object_or_404(Contestant, uid=uid)
        contestant.delete()
        return Response({"message": "Contestant deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
