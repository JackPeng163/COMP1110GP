from typing import List

from network import Mode, Route

class Filter:
    def routes_not_in_mode(self, mode: Mode, routes: List[Route]) -> List[Route]:
        routes_not_in_mode = []
        for route in routes:
            if route.mode != mode:
                routes_not_in_mode.append(route)
        return routes_not_in_mode
    def routes_in_mode(self, mode: Mode, routes: List[Route]) -> List[Route]:
        routes_in_mode = []
        for route in routes:
            if route.mode == mode:
                routes_in_mode.append(route)
        return routes_in_mode