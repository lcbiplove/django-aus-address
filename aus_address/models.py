from django.db import models
from django.contrib.gis.db import models as gis_models


class State(models.Model):
    """
    Model representing a state in Australia.
    Each state has a unique name and abbreviation.
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

    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=3, choices=STATE_CHOICES, unique=True)

    def __str__(self):
        return self.get_abbreviation_display()


class Suburb(gis_models.Model):
    """
    Model representing a suburb in Australia.
    Each suburb is associated with a state and has a unique name within that state.
    """
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    geometry = gis_models.PolygonField()
    centroid = gis_models.PointField()

    class Meta:
        unique_together = ("name", "state")

    def __str__(self):
        return f"{self.name}, {self.state.abbreviation}"


class Postcode(models.Model):
    """
    Model representing a postcode in Australia.
    Each postcode is associated with a state and can cover multiple suburbs.
    """
    code = models.CharField(max_length=4, unique=True)
    suburbs = models.ManyToManyField(Suburb)

    def __str__(self):
        return self.code


class Address(models.Model):
    """
    Model representing a full address in Australia.
    Each address includes a unit number, street name, suburb, postcode, and state.
    """
    unit = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    suburb = models.ForeignKey(Suburb, on_delete=models.CASCADE)
    postcode = models.ForeignKey(Postcode, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        address_parts = []
        if self.unit:
            address_parts.append(self.unit)
        if self.street:
            address_parts.append(self.street)
        address_parts.append(self.suburb.name)
        address_parts.append(self.state.abbreviation)
        address_parts.append(self.postcode.code)
        return ", ".join(address_parts)