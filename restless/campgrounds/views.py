from rest_framework import viewsets, mixins

from .models import Camper, Campsite
from .serializers import CamperSerializer, CampsiteSerializer


class CamperViewSet(viewsets.ModelViewSet):
    queryset = Camper.objects.all()
    serializer_class = CamperSerializer


class CampsiteViewSet(viewsets.ModelViewSet):
    queryset = Campsite.objects.all()
    serializer_class = CampsiteSerializer

