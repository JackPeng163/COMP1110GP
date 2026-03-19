from typing import List, Tuple

from journery_generator import Journey

class Ranker:
    def compute_stats(self, journey: Journey) -> Tuple[float, float, int]:
        raise NotImplementedError
    
    def rank(self, journeys: List[Journey], preference: str) -> List[Journey]:
        raise NotImplementedError