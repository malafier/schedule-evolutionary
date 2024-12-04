import random
from abc import ABC
from copy import deepcopy

from evolutionary.config import Config, MetaConfig
from evolutionary.crossover import crossover
from evolutionary.school_plan import SchoolPlan
from evolutionary.fixing_algorithm import fix_plan


class SelectionStrategy(ABC):
    def select_and_cross(self, parents: list, best_plan: SchoolPlan, size: int, config: Config) -> list[SchoolPlan]:
        pass


class RouletteSelection(SelectionStrategy):
    def select_and_cross(self, parents: list, best_plan: SchoolPlan, size: int, config: Config) -> list[SchoolPlan]:
        children = []
        if config.elitism:
            children.append(deepcopy(best_plan))

        crossover_rate = config.cross.crossover_rate
        sum_fitness = sum([plan.fitness for plan in parents])
        probabilities = [plan.fitness / sum_fitness for plan in parents]

        while len(children) < size:
            parent1, parent2 = random.choices(parents, probabilities, k=2)
            if random.random() < crossover_rate:
                child_plan_1, child_plan_2 = crossover(parent1.plans, parent2.plans, config.no_groups)
                if child_plan_1 is not None:
                    child = SchoolPlan(
                        config.no_groups,
                        fix_plan(child_plan_1, config.subjects, config.sub_to_teach)
                    )
                    children.append(child)
                if child_plan_2 is not None and len(children) < size:
                    child = SchoolPlan(
                        config.no_groups,
                        fix_plan(child_plan_2, config.subjects, config.sub_to_teach)
                    )
                    children.append(child)
        return children


class ChampionSelection(SelectionStrategy):
    def select_and_cross(self, parents: list, best_plan: SchoolPlan, size: int, config: Config) -> list[SchoolPlan]:
        children = []
        if config.elitism:
            children.append(deepcopy(best_plan))
        crossover_rate = config.cross.crossover_rate

        while len(children) < size:
            parent2 = random.choice(parents)
            if random.random() < crossover_rate:
                child_plan_1, child_plan_2 = crossover(best_plan.plans, parent2.plans, config.no_groups)
                if child_plan_1 is not None:
                    child = SchoolPlan(
                        config.no_groups,
                        fix_plan(child_plan_1, config.subjects, config.sub_to_teach)
                    )
                    children.append(child)
                if child_plan_2 is not None and len(children) < size:
                    child = SchoolPlan(
                        config.no_groups,
                        fix_plan(child_plan_2, config.subjects, config.sub_to_teach)
                    )
                    children.append(child)
        return children


class Generation:
    def __init__(self, config: Config, mconfig: MetaConfig, purge=False):
        self.gen_no: int = 0
        self.size: int = config.population_size
        self.config: Config = config
        self.meta: MetaConfig = mconfig
        self.purge: bool = purge
        self.population: list = []
        for _ in range(self.size):
            plan = SchoolPlan(config.no_groups)
            plan.generate(config)
            self.population.append(plan)

    def evaluate(self):
        for plan in self.population:
            plan.evaluate(self.config)

        self.population.sort(key=lambda x: x.fitness, reverse=True)

        # scale
        for pop in self.population:
            if pop.fitness < 0:
                pop.fitness = 0

    def best_plan(self) -> SchoolPlan:
        return max(self.population, key=lambda x: x.fitness)

    def worst_plan(self) -> SchoolPlan:
        return min(self.population, key=lambda x: x.fitness)

    def all(self):
        return [plan.as_dict() for plan in self.population]

    def statistics(self) -> dict:
        return {
            "max": self.best_plan().fitness,
            "avg": sum([plan.fitness for plan in self.population]) / self.size,
            "min": self.worst_plan().fitness
        }

    def selection_crossover(self, strategy: SelectionStrategy = RouletteSelection()):
        # selection
        self.population.sort(key=lambda x: x.fitness)
        best_plan = self.best_plan()

        # crossover
        self.population = strategy.select_and_cross(self.population, best_plan, self.size, self.config)
        self.gen_no += 1

    def mutate(self):
        for i in range(self.size - 1):
            if random.random() <= self.config.cross.mutation_rate:
                self.population[i].mutate(self.config)
