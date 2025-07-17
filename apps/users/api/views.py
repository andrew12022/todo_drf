from rest_framework import viewsets

from apps.users.api.serializers import UserSerializer
from apps.users.models import User


class UserViewSet(viewsets.ModelViewSet):
    """."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
