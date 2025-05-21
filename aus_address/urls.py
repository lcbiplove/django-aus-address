from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StateViewSet, LocationViewSet, LocationGeoViewSet

router = DefaultRouter()
router.register(r'states', StateViewSet)
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'locations-geo', LocationGeoViewSet, basename='location-geo')

urlpatterns = [
    path('', include(router.urls)),
]