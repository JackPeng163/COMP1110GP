from typing import List, Set

from src.network import Route, Stop, Network, Mode

class Journey:
    def __init__(self):
        self.routes: List[Route] = []
        self.score = 0.0

    def set_score(self, score: float) -> None:
        self.score = score

    def append_route(self, route: Route) -> None:
        self.routes.append(route)
    
    def pop_last_route(self) -> None:
        self.routes.pop(-1)

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

    def num_transfers(self) -> int:
        cnt_walk_to_walk = 0
        for i in range(len(self.routes) - 1):
            if self.routes[i].mode == Mode.WALKING and self.routes[i + 1].mode == Mode.WALKING:
                cnt_walk_to_walk += 1
        return len(self.routes) - cnt_walk_to_walk - 1

    def num_routes(self) -> int:
        return len(self.routes)
        
    def copy(self) -> "Journey":
        new_journey = Journey()
        new_journey.routes = self.routes[:]
        return new_journey


class Generator:
    def __init__(self, network: Network):
        self.network = network
        self.journeys: List[Journey] = []

    def _dfs(self, start: Stop, end: Stop, current_journey: Journey, visited: Set[Stop]) -> None:
        if start == end and len(current_journey.get_routes()) > 0:
            self.journeys.append(current_journey.copy())
            return

        routes_from_current = self.network.get_routes_from(start)
        
        for route in routes_from_current:
            next_stop = route.get_end()
            if next_stop in visited:
                continue
            visited.add(next_stop)
            current_journey.append_route(route)

            self._dfs(next_stop, end, current_journey, visited)

            visited.remove(next_stop)
            current_journey.pop_last_route()
    
    def _filter_pareto_optimal(self) -> None:
        pareto_optimal = []
        for journey in self.journeys:
            is_dominated = False
            for other in self.journeys:
                if other is journey:
                    continue
                if (other.total_duration() <= journey.total_duration() and 
                    other.total_cost() <= journey.total_cost() and
                    other.num_transfers() <= journey.num_transfers() and
                    (other.total_duration() < journey.total_duration() or 
                     other.total_cost() < journey.total_cost() or
                     other.num_transfers() < journey.num_transfers())):
                    is_dominated = True
                    break
            if not is_dominated:
                pareto_optimal.append(journey)
        self.journeys = pareto_optimal
    
    def _remove_duplicate_journeys(self) -> None:
        # 删除重复的journey
        unique_journeys = []
        for journey in self.journeys:
            for other_journey in unique_journeys:
                if journey.get_routes() == other_journey.get_routes():
                    break
            else:
                unique_journeys.append(journey)
        self.journeys = unique_journeys
    
    def generate(self, start: Stop, end: Stop) -> List[Journey]:
        # 每次生成前清空缓存，避免不同查询之间互相污染结果。
        self.journeys = []

        # 生成所有可能的journey
        self._dfs(start, end, Journey(), set[Stop]([start]))
        self._filter_pareto_optimal()
        self._remove_duplicate_journeys()
        return self.journeys