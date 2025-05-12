from django.contrib import admin
from .models import State, Suburb, Postcode, Address

admin.site.register(State)
admin.site.register(Suburb)
admin.site.register(Postcode)
admin.site.register(Address)