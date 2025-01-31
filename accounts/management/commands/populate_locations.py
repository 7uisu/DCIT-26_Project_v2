from django.core.management.base import BaseCommand
from app.models import CountryOfBirth, Region, Province, CityMunicipality, Barangay, PostalCode

class Command(BaseCommand):
    help = 'Populates location data like countries, regions, provinces, cities, etc.'

    def handle(self, *args, **kwargs):
        # Data for CALABARZON (Region IV-A) with all provinces, cities, barangays, and postal codes.
        countries = [
            {
                'name': 'Philippines',
                'regions': [
                    {
                        'name': 'Region IV-A (CALABARZON)',
                        'provinces': [
                            {
                                'name': 'Cavite',
                                'cities': [
                                    {
                                        'name': 'Bacoor',
                                        'barangays': [
                                            {'name': 'Molino 1', 'postal_code': '4102'},
                                            {'name': 'Molino 2', 'postal_code': '4103'},
                                            {'name': 'Molino 3', 'postal_code': '4104'},
                                            # Add more barangays...
                                        ]
                                    },
                                    {
                                        'name': 'Dasmariñas',
                                        'barangays': [
                                            {'name': 'Dasmariñas Central', 'postal_code': '4114'},
                                            # Add more barangays...
                                        ]
                                    },
                                    # Add more cities...
                                ]
                            },
                            {
                                'name': 'Laguna',
                                'cities': [
                                    {
                                        'name': 'Santa Rosa',
                                        'barangays': [
                                            {'name': 'Balibago', 'postal_code': '4026'},
                                            {'name': 'Dona Josefa', 'postal_code': '4027'},
                                            # Add more barangays...
                                        ]
                                    },
                                    {
                                        'name': 'San Pedro',
                                        'barangays': [
                                            {'name': 'Longos', 'postal_code': '4023'},
                                            {'name': 'Cabay', 'postal_code': '4024'},
                                            # Add more barangays...
                                        ]
                                    },
                                    # Add more cities...
                                ]
                            },
                            {
                                'name': 'Batangas',
                                'cities': [
                                    {
                                        'name': 'Batangas City',
                                        'barangays': [
                                            {'name': 'Poblacion', 'postal_code': '4200'},
                                            {'name': 'Alangilan', 'postal_code': '4201'},
                                            # Add more barangays...
                                        ]
                                    },
                                    # Add more cities...
                                ]
                            },
                            {
                                'name': 'Rizal',
                                'cities': [
                                    {
                                        'name': 'Antipolo',
                                        'barangays': [
                                            {'name': 'Cupang', 'postal_code': '1870'},
                                            {'name': 'Dela Paz', 'postal_code': '1871'},
                                            # Add more barangays...
                                        ]
                                    },
                                    {
                                        'name': 'Cainta',
                                        'barangays': [
                                            {'name': 'San Juan', 'postal_code': '1900'},
                                            # Add more barangays...
                                        ]
                                    },
                                    # Add more cities...
                                ]
                            },
                            {
                                'name': 'Quezon',
                                'cities': [
                                    {
                                        'name': 'Lucena',
                                        'barangays': [
                                            {'name': 'Dalahican', 'postal_code': '4300'},
                                            {'name': 'Ibabang Dupay', 'postal_code': '4301'},
                                            # Add more barangays...
                                        ]
                                    },
                                    {
                                        'name': 'Tayabas',
                                        'barangays': [
                                            {'name': 'Bayan', 'postal_code': '4331'},
                                            {'name': 'Candelaria', 'postal_code': '4332'},
                                            # Add more barangays...
                                        ]
                                    },
                                    # Add more cities...
                                ]
                            },
                            {
                                'name': 'Quezon City',  # Include any specific cities that need to be added
                                'cities': [
                                    {
                                        'name': 'Quezon City',
                                        'barangays': [
                                            {'name': 'New Manila', 'postal_code': '1100'},
                                            {'name': 'Cubao', 'postal_code': '1101'},
                                            # Add more barangays...
                                        ]
                                    },
                                    # Add more cities...
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

        # Loop through the countries and populate
        for country_data in countries:
            country = CountryOfBirth.objects.create(name=country_data['name'])

            for region_data in country_data['regions']:
                region = Region.objects.create(name=region_data['name'])

                for province_data in region_data['provinces']:
                    province = Province.objects.create(name=province_data['name'], region=region)

                    for city_data in province_data['cities']:
                        city = CityMunicipality.objects.create(name=city_data['name'], province=province)

                        for barangay_data in city_data['barangays']:
                            barangay = Barangay.objects.create(name=barangay_data['name'], city_municipality=city)

                            # Create postal code for each barangay
                            PostalCode.objects.create(code=barangay_data['postal_code'], city_municipality=city)

        self.stdout.write(self.style.SUCCESS('Successfully populated location data for CALABARZON.'))
 