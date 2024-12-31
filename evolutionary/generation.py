import random
from copy import deepcopy

from evolutionary.config import Config, MetaConfig
from evolutionary.fixing_algorithm import fix_plan
from evolutionary.school_plan import SchoolPlan
from evolutionary.selection import RouletteSelection


class Generation:
    def __init__(self, config: Config, mconfig: MetaConfig, plans: list[SchoolPlan] | None = None, gen_no: int = 0):
        self.gen_no: int = gen_no
        self.size: int = config.population_size
        self.config: Config = config
        self.meta: MetaConfig = mconfig

        self.population: list = plans
        if plans is None:
            self.population = []
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

    def statistics(self) -> dict:
        return {
            "gen": self.gen_no,
            "max": self.best_plan().fitness,
            "avg": sum([plan.fitness for plan in self.population]) / self.size,
            "min": self.worst_plan().fitness
        }

    def next_gen(self):
        # Fitness scaling
        if isinstance(self.meta.selection_strategy, RouletteSelection):
            f_min = self.worst_plan().fitness
            f_max = self.best_plan().fitness
            f_avg = sum([pop.fitness for pop in self.population]) / self.size
            C = self.config.C

            if C == 1:
                self.config.C = 1.01
                C = 1.01

            if f_min > (C * f_avg - f_max) / (C - 1.0):
                delta = f_max - f_avg
                a = (C - 1.0) * f_avg / delta
                b = f_avg * (f_max - C * f_avg) / delta
            else:
                delta = f_avg - f_min
                a = f_avg / delta
                b = - f_min * f_avg / delta

            for plan in self.population:
                plan.fitness = a * plan.fitness + b

        # Evolutionary step
        best_plan = deepcopy(self.best_plan())
        children = []

        if self.config.elitism:
            children.append(best_plan)

        while len(children) < self.size:
            parent1, parent2 = self.meta.selection_strategy.select(parents=self.population, config=self.config)
            if parent1 is None or parent1 == parent2:
                continue

            child_plan_1, child_plan_2 = self.meta.crossover_strategy.cross(
                parent1.plans, parent2.plans, self.config.no_groups
            )
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

    # Second fixing algorithm
    def fix(self):
        for pop in self.population:
            pop.fix(self.config)
