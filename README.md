# Australian Address API

A powerful Django-based REST API that provides comprehensive access to Australian address data with advanced geospatial capabilities. This API serves as a reliable source for Australian suburbs, postcodes, and states, complete with precise geographical coordinates. Whether you're building a location-based service, implementing address validation, or creating a mapping application, this API provides the essential data you need.

## Data Source

This API uses the comprehensive Australian postcode database provided by [Matthew Proctor](https://www.matthewproctor.com/australian_postcodes). The database includes:
- 18,526+ entries covering all Australian states and territories
- Precise geographical coordinates (latitude/longitude)
- Up-to-date postcode and suburb information
- Additional metadata including SA3/SA4 regions, electorates, and more

The data is regularly updated and maintained by the community, ensuring accuracy and completeness.

## Purpose

This API is designed to solve common challenges in Australian address management:

- **Address Validation**: Verify and validate Australian addresses
- **Location Search**: Find suburbs and postcodes with precise geographical data
- **Geospatial Analysis**: Perform location-based queries and distance calculations
- **Data Integration**: Easily integrate Australian address data into your applications
- **Mapping Applications**: Support for GeoJSON format makes it perfect for mapping solutions

## Key Features

- **Complete Australian Coverage**
  - All states and territories (18,526+ entries)
  - Comprehensive suburb and postcode database
  - Accurate geographical coordinates
  - Regular updates from the community

- **Advanced Search Capabilities**
  - Full-text search across suburbs and postcodes
  - State-based filtering
  - Geospatial radius search
  - Flexible ordering and pagination

- **Developer-Friendly**
  - RESTful API design
  - GeoJSON support for mapping applications
  - Comprehensive filtering options
  - Clear and consistent response format

## API Endpoints

### States
- `GET /states/` - Retrieve all Australian states and territories
- `GET /states/{id}/` - Get detailed information about a specific state
- Search states by name or abbreviation (e.g., "NSW", "Victoria")

### Locations
- `GET /locations/` - Access the complete location database
- `GET /locations/{id}/` - Get detailed information about a specific location
- Advanced filtering options:
  - By suburb name
  - By postcode
  - By state
  - By geographical coordinates with radius search

### GeoJSON Endpoints
- `GET /locations-geo/` - Get location data in GeoJSON format
- Perfect for mapping applications
- Supports all standard location filtering options

## Query Parameters

### Location Search
- `suburb` - Find locations by suburb name (e.g., "Sydney")
- `postcode` - Filter by postcode (e.g., "2000")
- `state` - Filter by state abbreviation (e.g., "NSW")
- `lat` - Center point latitude for radius search
- `lng` - Center point longitude for radius search
- `distance` - Search radius in kilometers

### Pagination
- `page` - Page number (default: 1)
- `page_size` - Results per page (default: 100, max: 100)

### Ordering
- `ordering` - Sort results by field (e.g., `suburb`, `postcode`)

## Data Model

### State
- `abbreviation` - Official state/territory code (e.g., "NSW", "VIC")
- `name` - Full state/territory name

### Location
- `postcode` - 4-digit Australian postcode
- `suburb` - Suburb name
- `state` - Associated state/territory
- `point` - Precise geographical coordinates
- `latitude` - Easy access to latitude value
- `longitude` - Easy access to longitude value

## Example Usage

### Retrieve All States
```http
GET /states/
```

### Find Suburbs by Postcode
```http
GET /locations/?postcode=2000
```

### Search Locations Near Sydney CBD
```http
GET /locations/?lat=-33.8688&lng=151.2093&distance=10
```

### Get NSW Locations in GeoJSON Format
```http
GET /locations-geo/?state=NSW
```

## Technical Requirements

### Database Requirements
- **PostgreSQL with PostGIS extension** (Required)
  - PostGIS is essential for geospatial functionality
  - Minimum PostgreSQL version: 12.0
  - Minimum PostGIS version: 3.0
  - The application will not work without PostGIS

### Python Dependencies
- Python 3.8 or higher
- Django 5.2.1
- Django REST Framework 3.15.2
- Django REST Framework GIS 1.1
- psycopg2-binary 2.9.10 (PostgreSQL adapter)
- Other dependencies as listed in requirements.txt

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd django_aus_address
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install and configure PostgreSQL with PostGIS:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib postgis

   # macOS (using Homebrew)
   brew install postgresql postgis

   # Windows
   # Download and install from https://postgis.net/windows_downloads/
   ```

5. Create a PostgreSQL database with PostGIS extension:
   ```sql
   CREATE DATABASE aus_address;
   \c aus_address
   CREATE EXTENSION postgis;
   ```

6. Configure your database settings in settings.py:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.contrib.gis.db.backends.postgis',
           'NAME': 'aus_address',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

7. Run migrations:
   ```bash
   python manage.py migrate
   ```

9. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Contributing

We welcome contributions to improve this API! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure your code follows our coding standards and includes appropriate tests.

## License

[Add your license information here]

## Support

For support, please [add your preferred support method here]

## Acknowledgments

- Data source: [Matthew Proctor's Australian Postcodes Database](https://www.matthewproctor.com/australian_postcodes)
- The community contributors who help maintain and update the postcode database