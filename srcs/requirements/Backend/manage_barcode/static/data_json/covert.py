import json
import re

def parse_stations(stations_lines):
    stations = []
    for line in stations_lines:
        match = re.match(r"Order: (\d+), ID: (\d+), Name: (.*?), Terminus: (True|False)", line)
        if match:
            order, id_, name, terminus = match.groups()
            stations.append({
                "Order": int(order),
                "ID": int(id_),
                "Name": name.strip(),
                "Terminus": terminus == "True"
            })
    return stations

def convert_txt_to_json(txt_file, json_file):
    with open(txt_file, 'r') as file:
        lines = file.readlines()
    
    data = {}
    city = None
    route = None
    stations_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("City:"):
            if city and route:
                route["Stations"] = parse_stations(stations_lines)
                if city not in data:
                    data[city] = []
                data[city].append(route)
            
            city = line.split("City:")[1].strip()
            route = None
            stations_lines = []
        elif line.startswith("Route Name:"):
            if route:
                route["Stations"] = parse_stations(stations_lines)
                if city not in data:
                    data[city] = []
                data[city].append(route)
                
            route = {
                "Route Name": line.split("Route Name:")[1].strip(),
                "Frequency": None,
                "Travel Time": None,
                "Number Of Buses": None,
                "Departure": None,
                "Stations": []
            }
            stations_lines = []
        elif line.startswith("Frequency:"):
            route["Frequency"] = int(line.split("Frequency:")[1].strip())
        elif line.startswith("Travel Time:"):
            route["Travel Time"] = int(line.split("Travel Time:")[1].strip())
        elif line.startswith("Number Of Buses:"):
            route["Number Of Buses"] = int(line.split("Number Of Buses:")[1].strip())
        elif line.startswith("Departure:"):
            departure_str = line.split("Departure:")[1].strip().strip('[]')
            route["Departure"] = [time.strip().strip("'") for time in departure_str.split(',')]
        elif line.startswith("Stations:"):
            continue
        else:
            stations_lines.append(line)
    
    if route:
        route["Stations"] = parse_stations(stations_lines)
        if city not in data:
            data[city] = []
        data[city].append(route)
    
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

# Usage
convert_txt_to_json('data.txt', 'output.json')
