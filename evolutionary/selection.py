import random
from abc import ABC

from evolutionary.config import Config
from evolutionary.school_plan import SchoolPlan


class SelectionStrategy(ABC):
    def select(self, parents: list[SchoolPlan], config: Config) -> (SchoolPlan, SchoolPlan):
        pass

    def __name__(self):
        pass

    def __str__(self):
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

    def __str__(self):
        return "RouletteSelection"


class TournamentSelection(SelectionStrategy):
    def select(self, parents: list[SchoolPlan], config: Config) -> (SchoolPlan, SchoolPlan):
        if random.random() < config.cross.crossover_rate:
            return None, None

        arena1 = random.choices(parents, k=config.k)
        arena2 = random.choices(parents, k=config.k)

        return (
            max(arena1, key=lambda x: x.fitness),
            max(arena2, key=lambda x: x.fitness)
        )

    def __name__(self):
        return "TournamentSelection"

    def __str__(self):
        return "TournamentSelection"


def str_to_class(name):
    if name == "RouletteSelection":
        return RouletteSelection
    else:
        return TournamentSelection()
