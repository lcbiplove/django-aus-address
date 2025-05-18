from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import State, Location

class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')
    list_filter = ('abbreviation',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('abbreviation', 'name')
        }),
    )

class LocationAdmin(GISModelAdmin):
    list_display = ('suburb', 'postcode', 'state', 'latitude', 'longitude')
    search_fields = ('suburb', 'postcode', 'state__name', 'state__abbreviation')
    list_filter = ('state',)
    ordering = ('suburb',)
    readonly_fields = ('latitude', 'longitude')
    list_select_related = ('state',)
    
    default_lon = 133.7751
    default_lat = -25.2744
    default_zoom = 4
    display_wkt = False
    display_srid = False
    
    fieldsets = (
        ('Location Info', {
            'fields': ('suburb', 'postcode', 'state')
        }),
        ('Geospatial Data', {
            'fields': ('point', 'latitude', 'longitude'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('state')

admin.site.register(State, StateAdmin)
admin.site.register(Location, LocationAdmin)