from rest_framework import serializers
from .models import Camper, Campsite, CampHost, Campground


class CamperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Camper
        fields = ('id', 'name', 'campsite')


class CampsiteSerializer(serializers.ModelSerializer):
    campers = CamperSerializer

    class Meta:
        model = Campsite
        fields = ('id', 'name', 'tent_only', 'campground', 'campers', 'location')
        depth = 1


class CampgroundSerializer(serializers.ModelSerializer):
    campsites = CampsiteSerializer

    class Meta:
        model = Campground
        fields = ('id', 'name', 'campsites')
        depth = 2

class CampHostSerializer(serializers.ModelSerializer):
    campgrounds = CampgroundSerializer

    class Meta:
        model = CampHost
        fields = ('id', 'name', 'campgrounds')
