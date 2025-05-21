from rest_framework import serializers
from .models import State, Location


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)
    formatted_address = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ('state', 'formatted_address')

    def get_formatted_address(self, obj):
        return f"{obj.suburb}, {obj.state.abbreviation} {obj.postcode}"


class LocationGeoSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="Feature", read_only=True)
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()
    formatted_address = serializers.SerializerMethodField()


    class Meta:
        model = Location
        fields = ('type', 'geometry', 'properties', 'formatted_address')

    def get_geometry(self, obj):
        return {
            "type": "Point",
            "coordinates": [obj.point.x, obj.point.y] if obj.point else None
        }

    def get_properties(self, obj):
        return {
            "id": obj.id,
            "suburb": obj.suburb,
            "postcode": obj.postcode,
            "state": obj.state.abbreviation
        }
    
    def get_formatted_address(self, obj):
        return f"{obj.suburb}, {obj.state.abbreviation} {obj.postcode}"