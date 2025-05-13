from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import State, Suburb, Postcode, Address

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')
    ordering = ('name',)
    list_per_page = 20


@admin.register(Suburb)
class SuburbAdmin(GISModelAdmin):
    list_display = ('name', 'state', 'display_location')
    list_filter = ('state',)
    search_fields = ('name', 'state__name', 'state__abbreviation')
    raw_id_fields = ('state',)
    list_select_related = ('state',)
    list_per_page = 30
    
    def display_location(self, obj):
        if obj.location:
            return f"{obj.location.y:.4f}, {obj.location.x:.4f}"
        return "No coordinates"
    display_location.short_description = "Lat, Long"


@admin.register(Postcode)
class PostcodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'suburbs_count', 'display_states')
    search_fields = ('code', 'suburbs__name')
    filter_horizontal = ('suburbs',)
    list_per_page = 30
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('suburbs')
    
    def suburbs_count(self, obj):
        return obj.suburbs.count()
    suburbs_count.short_description = "Suburbs Count"
    
    def display_states(self, obj):
        states = set(suburb.state.abbreviation for suburb in obj.suburbs.all())
        return ", ".join(sorted(states))
    display_states.short_description = "States"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'unit', 'suburb', 'postcode', 'state')
    list_filter = ('state', 'postcode', 'suburb__state')
    search_fields = (
        'street', 
        'unit', 
        'suburb__name', 
        'postcode__code',
        'state__name',
        'state__abbreviation'
    )
    raw_id_fields = ('suburb', 'postcode', 'state')
    autocomplete_fields = ('suburb', 'postcode', 'state')
    list_select_related = ('suburb', 'postcode', 'state')
    list_per_page = 50