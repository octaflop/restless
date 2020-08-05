from rest_framework import serializers
from .models import Camper, Campsite


class CamperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Camper
        fields = ('id', 'name')


class CampsiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campsite
        fields = ('id', 'name', 'tent_only', 'campground', 'campers')
