from rest_framework import viewsets, mixins

from .models import Camper, Campsite, Campground, CampHost
from .serializers import CamperSerializer, CampsiteSerializer, CampHostSerializer, CampgroundSerializer


class CamperViewSet(viewsets.ModelViewSet):
    queryset = Camper.objects.all()
    serializer_class = CamperSerializer

class CampsiteViewSet(viewsets.ModelViewSet):
    queryset = Campsite.objects.all()
    serializer_class = CampsiteSerializer


class CampHostViewSet(viewsets.ModelViewSet):
    queryset = CampHost.objects.all()
    serializer_class = CampHostSerializer


class CampgroundViewSet(viewsets.ModelViewSet):
    queryset = Campground.objects.all()
    serializer_class = CampgroundSerializer

