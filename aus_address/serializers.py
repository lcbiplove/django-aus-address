# serializers.py
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from django.contrib.gis.geos import Point
from .models import State, Suburb, Postcode, Address

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'abbreviation']

class SuburbSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)
    postcodes = serializers.SlugRelatedField(
        source='postcode_set',
        many=True,
        read_only=True,
        slug_field='code'
    )
    location = GeometryField()

    class Meta:
        model = Suburb
        fields = ['id', 'name', 'state', 'postcodes', 'location']

class PostcodeSerializer(serializers.ModelSerializer):
    suburbs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Postcode
        fields = ['code', 'suburbs']

class AddressSerializer(serializers.ModelSerializer):
    suburb = serializers.PrimaryKeyRelatedField(queryset=Suburb.objects.all())
    postcode = serializers.PrimaryKeyRelatedField(queryset=Postcode.objects.all())
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())

    class Meta:
        model = Address
        fields = ['id', 'unit', 'street', 'suburb', 'postcode', 'state']

    def validate(self, data):
        suburb = data.get('suburb')
        state = data.get('state')
        postcode = data.get('postcode')

        if suburb and state and suburb.state != state:
            raise serializers.ValidationError("State must match the suburb's state.")

        if postcode and suburb and not postcode.suburbs.filter(id=suburb.id).exists():
            raise serializers.ValidationError("Suburb must be in the selected postcode.")

        return data