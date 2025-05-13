from django.contrib.gis.geos import Point
from django.db import transaction
import csv
from .models import State, Suburb, Postcode

def populate_locations(data_file_path: str):
    with transaction.atomic():
        states = {}
        suburbs = {}
        postcodes = {}
        relationships = []

        with open(data_file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                postcode_str = row["postcode"].strip()
                locality = row["locality"].strip().title()
                state_abbr = row["state"].strip().upper()
                lon_str = row["long"].strip()
                lat_str = row["lat"].strip()

                if lon_str in ("0", "") or lat_str in ("0", ""):
                    continue
                try:
                    lon = float(lon_str)
                    lat = float(lat_str)
                except ValueError:
                    continue

                if state_abbr not in states:
                    states[state_abbr] = dict(State.STATE_CHOICES).get(state_abbr, state_abbr)

                suburb_key = (locality, state_abbr)
                if suburb_key not in suburbs:
                    suburbs[suburb_key] = {
                        "state": state_abbr,
                        "location": Point(lon, lat, srid=4326)
                    }

                if postcode_str not in postcodes:
                    postcodes[postcode_str] = set()
                postcodes[postcode_str].add(suburb_key)
                relationships.append((postcode_str, suburb_key))

        State.objects.bulk_create([
            State(abbreviation=abbr, name=name) for abbr, name in states.items()
        ], ignore_conflicts=True)

        state_instances = {s.abbreviation: s for s in State.objects.all()}

        suburb_objs = [
            Suburb(
                name=name,
                state=state_instances[data["state"]],
                location=data["location"]
            ) for (name, state_abbr), data in suburbs.items()
        ]
        Suburb.objects.bulk_create(suburb_objs, ignore_conflicts=True)

        suburb_instances = {
            (s.name, s.state.abbreviation): s for s in Suburb.objects.all()
        }

        Postcode.objects.bulk_create([
            Postcode(code=code) for code in postcodes.keys()
        ], ignore_conflicts=True)

        postcode_instances = {p.code: p for p in Postcode.objects.all()}

        ThroughModel = Postcode.suburbs.through
        through_objs = []
        for postcode_str, (locality, state_abbr) in relationships:
            postcode = postcode_instances.get(postcode_str)
            suburb = suburb_instances.get((locality, state_abbr))
            if postcode and suburb:
                through_objs.append(ThroughModel(postcode_id=postcode.id, suburb_id=suburb.id))
        
        ThroughModel.objects.bulk_create(through_objs, ignore_conflicts=True)