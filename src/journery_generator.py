from typing import List

from network import Route, Stop, Network

class Journey:
    def __init__(self):
        self.routes: List[Route] = []

    def add_route(self, Route: Route) -> None:
        self.routes.append(Route)

    def get_routes(self) -> List[Route]:
        return self.routes

    def total_duration(self) -> float:
        total_duration = 0.0
        for route in self.routes:
            total_duration += route.duration
        return total_duration

    def total_cost(self) -> float:
        total_cost = 0.0
        for route in self.routes:
            total_cost += route.cost
        return total_cost

    def num_routes(self) -> int:
        return len(self.routes)


class Generator:
    def _dfs(self, network: Network, current_stop: Stop, dest: Stop, visited: List[Stop], current_journey: Journey, max_depth: int) -> None:
        raise NotImplementedError
    
    def generate(self, network: Network, origin_id: str, dest_id: str, max_depth: int) -> List[Journey]:
        raise NotImplementedError