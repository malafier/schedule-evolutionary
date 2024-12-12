import random
from copy import deepcopy

from evolutionary.config import Config, MetaConfig
from evolutionary.crossover import crossover
from evolutionary.school_plan import SchoolPlan
from evolutionary.fixing_algorithm import fix_plan
from evolutionary.selection import SelectionStrategy, RouletteSelection


class Generation:
    def __init__(self, config: Config, mconfig: MetaConfig):
        self.gen_no: int = 0
        self.size: int = config.population_size
        self.config: Config = config
        self.meta: MetaConfig = mconfig
        self.population: list = []
        for _ in range(self.size):
            plan = SchoolPlan(config.no_groups)
            plan.generate(config)
            self.population.append(plan)

    def evaluate(self):
        for plan in self.population:
            plan.evaluate(self.config)

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

    def next_gen(self, strategy: SelectionStrategy = RouletteSelection()):
        best_plan = deepcopy(self.best_plan())
        children = []

        if self.config.elitism:
            children.append(best_plan)


        while len(children) < self.size:
            parent1, parent2 = strategy.select(self.population, self.config)
            if parent1 is None or parent1 == parent2:
                continue

            child_plan_1, child_plan_2 = crossover(parent1.plans, parent2.plans, self.config.no_groups)
            if child_plan_1 is not None:
                child = SchoolPlan(
                    self.config.no_groups,
                    fix_plan(child_plan_1, self.config.subjects, self.config.sub_to_teach)
                )
                if random.random() <= self.config.cross.mutation_rate:
                    child.mutate(self.config)
                children.append(child)

            if child_plan_2 is not None and len(children) < self.size:
                child = SchoolPlan(
                    self.config.no_groups,
                    fix_plan(child_plan_2, self.config.subjects, self.config.sub_to_teach)
                )
                if random.random() <= self.config.cross.mutation_rate:
                    child.mutate(self.config)
                children.append(child)

        self.population = children
        self.gen_no += 1
