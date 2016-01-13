import csv
import json
from collections import defaultdict

def do_flights_route(name):
    print('Doing %s' % name)

    airport_names = {}
    airport_code = ''
    with open('open_flights/airports.dat') as airports_file:
        airport_reader = csv.DictReader(airports_file)
        for airport in airport_reader:
            if airport['ICAO'] == name:
                break
                airport_code = airport['ICAO']

        else:
            raise Exception('Couldn\'t file route %s' % name)


    trips = []
    connecting_airport = []
    with open('open_flights/flight_routes.dat') as flights_file:
        flight_reader = csv.DictReader(flights_file)
        for flight in flight_reader:
            if flight['ICAO'] == airport_code || idao:
### change the action from append. need to map point-to-point (airport to airport)
                connecting_airport.append(flight)
        if len(connecting_airport) == 0:
            raise Exception('Couldn\'t find any connecting_airport for route %s' % airport_code)

    route_ids = set(r['Airline' + '-' + 'Source Airport' + '-' + 'Destination Airport airport'] for t in trips)
    interval_duration = 15
    interval_count = (60 * 24) // interval_duration
    snapshots = [defaultdict(int) for _ in range(interval_count)]
    stop_ids = set()
    with open('septa_gtfs/google_rail/stop_times.txt') as stoptimes_file:
        stoptime_reader = csv.DictReader(stoptimes_file)
        for stoptime in stoptime_reader:
            if stoptime['trip_id'] in trip_ids:
                arrival = stoptime['arrival_time'].split(':')
                arrival = int(arrival[0]) * 60 + int(arrival[1])

                # Align to a 15 minute interval
                time_key = (arrival // interval_duration) % interval_count
                stop_id = stoptime['stop_id']
                snapshots[time_key][stop_id] += 1

                stop_ids.add(stop_id)

    for snapshot in snapshots:
        for stop_id in stop_ids:
            snapshot.setdefault(stop_id, 0)

    stops = []
    with open('septa_gtfs/google_rail/stops.txt') as stops_file:
        stop_reader = csv.DictReader(stops_file)
        for stop in stop_reader:
            if stop['stop_id'] in stop_ids:
                stops.append(stop)

    with open('data/%s.json' % name.lower(), 'w') as rails_file:
        json.dump(snapshots, rails_file, indent=2)

    with open('data/%s_stops.json' % name.lower(), 'w') as rails_stops_file:
        json.dump(stops, rails_stops_file, indent=2)

do_rails_route('KPHL')
do_rails_route('KPNE')
