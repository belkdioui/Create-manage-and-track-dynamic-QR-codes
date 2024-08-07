import re
import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_time
from django.core.exceptions import ObjectDoesNotExist
from manage_barcode.models import FormData , City, Bus, Station


def check_errors(type, data):
    EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    PHONE_REGEX = r"(^(?:05|06|07)\d{8}$|^\+212\d{9}$)"

    errors = {}
    if type=="reset_password":
        if not re.match("^.{8,}$" , data["password"]):
            errors["err_pass"]="password should contain at least 8 characters"
        if not re.match(data["password"], data["cpassword"]):
            errors["err_pass_c"]="password doesn't match confirm password"
    elif type=="sign_up":
        if any(char.isdigit() for char in data["fname"]):
            errors["err_fname"]="First Name invalid "
        if any(char.isdigit() for char in data["lname"]):
            errors["err_lname"]="Last Name invalid "
        if not re.match(EMAIL_REGEX, data["email"]):
            errors["err_email"]="email invalid "
        if not re.match(PHONE_REGEX, data["tel"]):
            errors["err_tel"]="Phone Number invalid "
        if not re.match("^.{8,}$" , data["password"]):
            errors["err_pass"]="password should contain at least 8 characters"
        if not re.match(data["password"], data["cpassword"]):
            errors["err_pass_c"]="password doesn't match confirm password"
        try:
            FormData.objects.get(email=data["email"])
            errors["err_email_ex"] = "email already exists"
        except FormData.DoesNotExist:
            pass

    return errors

def fill_json_in_db(file_path):
    data = load_json_data(file_path)
    for city_name, buses in data.items():
        city, created = City.objects.get_or_create(name=city_name)
        for bus_data in buses:
            bus, created = Bus.objects.get_or_create(
                city=city,
                name=bus_data['Route Name'],
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
                        bus = bus,
                        defaults={
                            'location': station_data['Name'],
                            'terminus': station_data['Terminus'],
                            'order': station_data['Order'],
                        }
                    )




def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
