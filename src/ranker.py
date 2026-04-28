from enum import Enum
from typing import List

from src.journey_generator import Journey

class Weight(Enum):
    TIME_PREFERENCE = [0.6, 0.3, 0.1] #Time, Cost, Transfers
    COST_PREFERENCE = [0.3, 0.6, 0.1]
    TRANSFERS_PREFERENCE = [0.25, 0.25, 0.5]
    BALANCED_PREFERENCE = [0.4525, 0.4525, 0.05]

class Ranker:
    def _normalisation(self, value: float, min_value: float, max_value: float) -> float:
        if max_value == min_value:
            return 0.0
        return (value - min_value) / (max_value - min_value)
    def _normalised_matrix(self, journeys: List[Journey]) -> List[List[float]]:
        normalised_matrix = []
        max_duration = max(journey.total_duration() for journey in journeys)
        max_cost = max(journey.total_cost() for journey in journeys)
        max_transfer = max(journey.num_transfers() for journey in journeys)
        for journey in journeys:
            normalised_journey = []
            normalised_journey.append(self._normalisation(journey.total_duration(), 0, max_duration))
            normalised_journey.append(self._normalisation(journey.total_cost(), 0, max_cost))
            normalised_journey.append(self._normalisation(journey.num_transfers(), 0, max_transfer))
            normalised_matrix.append(normalised_journey)
        return normalised_matrix
    def _weighted_matrix(self, normalised_matrix: List[List[float]], weight: Weight) -> List[List[float]]:
        weighted_matrix = []
        for journey in normalised_matrix:
            weighted_journey = []
            for i in range(len(journey)):
                weighted_journey.append(journey[i] * weight.value[i])
            weighted_matrix.append(weighted_journey)
        return weighted_matrix
    def _score_journey(self, journeys: List[Journey], weight_matrix: List[List[float]]) -> List[Journey]:
        scores = [sum(journey) for journey in weight_matrix]
        for i in range(len(journeys)):
            journeys[i].set_score(scores[i])
        return journeys
    def rank(self, journeys: List[Journey], weight: Weight) -> List[Journey]:
        if not journeys:
            return []
        normalised_matrix = self._normalised_matrix(journeys)
        weighted_matrix = self._weighted_matrix(normalised_matrix, weight)
        scored_journeys = self._score_journey(journeys, weighted_matrix)
        # lower score is better.
        scored_journeys.sort(key=lambda x: x.score)
        return scored_journeys
