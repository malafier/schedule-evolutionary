from abc import ABC
import random

from evolutionary.config import Config
from evolutionary.school_plan import SchoolPlan


class SelectionStrategy(ABC):
    def select(self, parents: list, config: Config) -> (SchoolPlan, SchoolPlan):
        pass

    def __name__(self):
        pass


class RouletteSelection(SelectionStrategy):
    def select(self, parents: list[SchoolPlan], config: Config) -> (SchoolPlan, SchoolPlan):
        if random.random() < config.cross.crossover_rate:
            return None, None

        sum_fitness = sum([plan.fitness for plan in parents])
        probabilities = [plan.fitness / sum_fitness for plan in parents]

        return random.choices(parents, probabilities, k=2)

    def __name__(self):
        return "RouletteSelection"


class ChampionSelection(SelectionStrategy):
    def select(self, parents: list, config: Config) -> (SchoolPlan, SchoolPlan):
        if random.random() < config.cross.crossover_rate:
            return None, None

        arena1 = random.choices(parents, k=config.S)
        arena2 = random.choices(parents, k=config.S)

        return (
            max(arena1, key=lambda x: x.fitness),
            max(arena2, key=lambda x: x.fitness)
        )

    def __name__(self):
        return "ChampionSelection"
