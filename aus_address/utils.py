import csv
from django.contrib.gis.geos import Point
from .models import State, Location

def populate_locations(csv_path: str):
    """
    Load location data from CSV into the database
    Usage: Call this from an empty migration
    """
    state_map = {
        'ACT': 'Australian Capital Territory',
        'NSW': 'New South Wales',
        'NT': 'Northern Territory',
        'QLD': 'Queensland',
        'SA': 'South Australia',
        'TAS': 'Tasmania',
        'VIC': 'Victoria',
        'WA': 'Western Australia'
    }
    
    for abbrev, name in state_map.items():
        State.objects.get_or_create(abbreviation=abbrev, defaults={'name': name})

    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        batch = []
        
        for row in reader:
            try:
                if float(row['lat']) == 0 or float(row['long']) == 0:
                    continue
                    
                batch.append(Location(
                    postcode=row['postcode'],
                    suburb=row['locality'].title(),
                    state=State.objects.get(abbreviation=row['state']),
                    point=Point(float(row['long']), float(row['lat'])),
                ))
                
                if len(batch) >= 1000:
                    Location.objects.bulk_create(batch, ignore_conflicts=True)
                    batch = []
                    
            except (ValueError, KeyError) as e:
                print(f"Skipping row due to error: {e}")
                continue
        
        if batch:
            Location.objects.bulk_create(batch, ignore_conflicts=True)

    print(f"Successfully loaded locations from {csv_path}")