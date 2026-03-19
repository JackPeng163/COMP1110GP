from typing import List
from enum import Enum, auto

class Mode(Enum):
    WALKING = auto()
    BUS = auto()
    SUBWAY = auto()
    TRAIN = auto()
    AIRPLANE = auto()

class Stop:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name


class Route:
    def __init__(self, start: Stop, end: Stop, duration: float, cost: float, mode: Mode):
        self.start = start
        self.end = end
        self.duration = duration
        self.cost = cost
        self.mode = mode

    def get_start(self) -> Stop:
        return self.start

    def get_end(self) -> Stop:
        return self.end

    def get_duration(self) -> float:
        return self.duration

    def get_cost(self) -> float:
        return self.cost
    
    def get_mode(self) -> Mode:
        return self.mode


class Network:
    def __init__(self, stops: List[Stop] = None, routes: List[Route] = None):
        self.stops: List[Stop] = stops if stops is not None else []
        self.routes: List[Route] = routes if routes is not None else []

    def add_stop(self, stop: Stop) -> bool:
        self.stops.append(stop)
        return True

    def add_route(self, route: Route) -> bool:
        if route.start not in self.stops or route.end not in self.stops:
            print(f"Error: Route start or end stop not in network. Start: {route.start.get_id()}, End: {route.end.get_id()}")
            return False
        else:
            self.routes.append(route)
            return True

    def get_stop_by_id(self, id: str) -> Stop:
        for stop in self.stops:
            if stop.get_id() == id:
                return stop
        raise ValueError(f"Stop with ID {id} not found")

    def get_routes_from(self, stop: Stop) -> List[Route]:
        routes_from_stop = []
        for route in self.routes:
            if route.start == stop:
                routes_from_stop.append(route)
        return routes_from_stop

    def get_all_stops(self) -> List[Stop]:
        return self.stops