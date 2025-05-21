from re import sub
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from .models import State, Location
from .serializers import StateSerializer, LocationSerializer, LocationGeoSerializer

class DefaultPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'

class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.all().order_by('name')
    serializer_class = StateSerializer
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'abbreviation']

class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LocationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['suburb', 'postcode', 'state__name', 'state__abbreviation']
    ordering_fields = ['suburb', 'postcode']
    ordering = ['suburb']
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = Location.objects.select_related('state')
        
        state = self.request.query_params.get('state')
        suburb = self.request.query_params.get('suburb')
        postcode = self.request.query_params.get('postcode')
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        distance = self.request.query_params.get('distance')

        if state:
            queryset = queryset.filter(state__abbreviation=state)
        if suburb:
            queryset = queryset.filter(suburb=suburb)
        if postcode:
            queryset = queryset.filter(postcode=postcode)
        if lat and lng and distance:
            point = Point(float(lng), float(lat), srid=4326)
            queryset = queryset.filter(
                point__distance_lte=(point, Distance(km=float(distance)))
            )
            
        return queryset

class LocationGeoViewSet(LocationViewSet):
    serializer_class = LocationGeoSerializer
    pagination_class = DefaultPagination
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response({
            'type': 'FeatureCollection',
            'features': serializer.data
        })