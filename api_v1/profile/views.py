from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import ProfileSerializer

from profiles.models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing profiles
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]


class FriendView(viewsets.ViewSet):
    serializer_class = ProfileSerializer

    def retrieve(self, request, pk=None):
        """
        Get all the friends of a specific profile.
        """
        qs = Profile.objects.all()
        profile = get_object_or_404(qs, pk=pk)
        friends = list(
            map(
                lambda f: ProfileSerializer(
                    f, context={'request': request}).data,
                profile.friends.all()
            )
        )
        return Response(friends)

    @swagger_auto_schema(
        operation_description="Given two profileId, return the shorter connection between them using an array of Ids.",
        manual_parameters=[
            openapi.Parameter(
                "from_id",
                openapi.IN_PATH,
                description="Profile id",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "to_id",
                openapi.IN_PATH,
                description="Profile id",
                type=openapi.TYPE_INTEGER
            )
        ])
    @action(detail=False, methods=["get"], url_path=r'shorter-connection/(?P<from_id>\d+)/(?P<to_id>\d+)')
    def shorter_connection(self, request, from_id: int, to_id: int):

        result = Profile.shorter_connection(int(from_id), int(to_id))
        return Response(result)
