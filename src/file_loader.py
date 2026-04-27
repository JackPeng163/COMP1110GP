import csv
from typing import List

from src.network import Mode, Route, Stop, Network


class FileLoader:
    def _load_stops(self, filepath: str) -> List[Stop]:
        """
        Load stop data from a CSV file.
        CSV format: id,name
        """
        stops = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    stop = Stop(
                        id=row['id'].strip(),
                        name=row['name'].strip()
                    )
                    stops.append(stop)
            print(f"Successfully loaded {len(stops)} stops")
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
        except Exception as e:
            print(f"Error loading stops: {e}")
        
        return stops

    def _load_routes(self, filepath: str) -> List[Route]:
        """
        Load route data from a CSV file.
        CSV format: start_id,end_id,duration,cost,mode
        """
        routes = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # Create temporary Stop objects and replace them in build_network.
                    start_stop = Stop(row['start_id'].strip(), "")
                    end_stop = Stop(row['end_id'].strip(), "")
                    
                    route = Route(
                        start=start_stop,
                        end=end_stop,
                        duration=float(row['duration']),
                        cost=float(row['cost']),
                        mode=Mode[row['mode']]  # Convert string to Enum.
                    )
                    routes.append(route)
            print(f"Successfully loaded {len(routes)} routes")
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
        except KeyError as e:
            print(f"CSV format error: Missing column {e}")
        except Exception as e:
            print(f"Error loading routes: {e}")
        
        return routes
    
    def _validate_network(self, stops: List[Stop], routes: List[Route]) -> bool:
        """
        Validate network data integrity.
        - Ensure all route start/end points exist in the stop list.
        """
        stop_ids = {stop.id for stop in stops}
        for route in routes:
            if route.start.id not in stop_ids:
                print(f"Error: Route start stop {route.start.id} is not in the stop list")
                return False
            if route.end.id not in stop_ids:
                print(f"Error: Route end stop {route.end.id} is not in the stop list")
                return False
        return True

    def build_network(self, stops_file: str, routes_file: str) -> Network:
        stops: List[Stop] = self._load_stops(stops_file)
        routes: List[Route] = self._load_routes(routes_file)
        if not self._validate_network(stops, routes):
            print("Network data validation failed")
            return None

        # Replace temporary Stop objects with actual Stop objects from the network
        # to ensure object-based comparisons can correctly match outgoing routes.
        stop_by_id = {stop.id: stop for stop in stops}
        for route in routes:
            route.start = stop_by_id[route.start.id]
            route.end = stop_by_id[route.end.id]

        network = Network(stops=stops, routes=routes)
        return network