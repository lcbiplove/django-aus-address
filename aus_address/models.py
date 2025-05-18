from django.db import models
from django.contrib.gis.db import models as gis_models

class State(models.Model):
    """
    Simplified state model with just the essential fields
    """
    STATE_CHOICES = [
        ("ACT", "Australian Capital Territory"),
        ("NSW", "New South Wales"),
        ("NT", "Northern Territory"),
        ("QLD", "Queensland"),
        ("SA", "South Australia"),
        ("TAS", "Tasmania"),
        ("VIC", "Victoria"),
        ("WA", "Western Australia"),
    ]

    abbreviation = models.CharField(max_length=3, choices=STATE_CHOICES, unique=True)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class Location(gis_models.Model):
    """
    Single source of truth for all locations with geospatial capabilities
    """
    postcode = models.CharField(max_length=4, db_index=True)
    suburb = models.CharField(max_length=100, db_index=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='locations')
    point = gis_models.PointField(srid=4326, geography=True, spatial_index=True)
    
    class Meta:
        unique_together = ('postcode', 'suburb', 'state')
        ordering = ['suburb']

    def __str__(self):
        return f"{self.suburb}, {self.state.abbreviation} {self.postcode}"

    @property
    def latitude(self):
        return self.point.y if self.point else None

    @property
    def longitude(self):
        return self.point.x if self.point else None