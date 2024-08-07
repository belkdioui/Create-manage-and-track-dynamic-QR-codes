import json
from manage_barcode.models import Order_station , City, Bus, Station
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_time

def fill_json_in_db(file_path):
    data = load_json_data(file_path)
    for city_name, buses in data.items():
        city, created = City.objects.get_or_create(name=city_name)
        for bus_data in buses:
            bus, created = Bus.objects.get_or_create(
                city=city,
                number=bus_data['Route Name'],
                defaults={
                    'frequency': bus_data['Frequency'],
                    'depart_time': parse_time(bus_data['Departure'][0]),
                    'end_time': parse_time(bus_data['Departure'][1]),
                    'travel_time': bus_data['Travel Time'],
                    'number_of_buses': bus_data['Number Of Buses'],
                    }
            )
            for station_data in bus_data['Stations']:
                station, created = Station.objects.get_or_create(
                        station_id=station_data['ID'],
                        defaults={
                            'location': station_data['Name'],
                            'terminus': station_data['Terminus'],
                        }
                    )
                Order_station.objects.create(
                        bus=bus,
                        stat_id=station.station_id,
                        order=station_data['Order'],
                    )




def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

fill_json_in_db('data.json')
