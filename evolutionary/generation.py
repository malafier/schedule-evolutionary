import random
from abc import ABC

from evolutionary.config import Config, H_PER_DAY, Day
from evolutionary.school_plan import SchoolPlan


class CrossoverStrategy(ABC):
    def crossover(self, parents, best_plan, size, crossover_rate, config: Config):
        pass

    def cross(self, plan1, plan2, config):
        pass

    def valid_plans(self, plan1: SchoolPlan, plan2: SchoolPlan, config: Config) -> bool:
        return plan1.plans.keys() == plan2.plans.keys() and plan1.plans.keys() == config.head_teachers.keys() \
            and plan1.plans != plan2.plans


# TODO: zmienić na koło rulety
class SinglePointCrossover(CrossoverStrategy):
    def crossover(self, parents, best_plan, size, crossover_rate, config: Config):
        children = []
        while len(children) < size - 1:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            if random.random() < crossover_rate:
                child = self.cross(parent1, parent2, config)
                if child is not None:
                    children.append(child)
        children.append(best_plan)
        return children

    def cross(self, plan1, plan2, config):
        if not self.valid_plans(plan1, plan2, config):
            return None

        DIV_FACTOR = 0.5

        groups = config.head_teachers.keys()
        child = SchoolPlan(groups)
        for name in groups:
            for day in list(Day):
                for hour in range(H_PER_DAY):
                    lesson = plan2.plans[name][day.value + hour] if random.random() < DIV_FACTOR \
                        else plan1.plans[name][day.value + hour]
                    child.add_to_plan(config, name, day, hour, lesson)
        child.fill_plan(config)
        return child


# TODO: jw.
class DayCrossover(CrossoverStrategy):
    def crossover(self, parents, best_plan, size, crossover_rate, config: Config):
        children = []
        while len(children) < size - 1:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            if random.random() < crossover_rate:
                child = self.cross(parent1, parent2, config)
                if child is not None:
                    children.append(child)
        children.append(best_plan)
        return children

    def cross(self, plan1, plan2, config):
        if not self.valid_plans(plan1, plan2, config):
            return None

        DIV_FACTOR = 0.5

        groups = config.head_teachers.keys()
        child = SchoolPlan(groups)
        for name in groups:
            for day in list(Day):
                plan = plan2 if random.random() < DIV_FACTOR else plan1
                for hour in range(H_PER_DAY):
                    lesson = plan.plans[name][day.value + hour]
                    child.add_to_plan(config, name, day, hour, lesson)
        child.fill_plan(config)
        return child


class ChampionCrossover(CrossoverStrategy):
    def crossover(self, parents, best_plan, size, crossover_rate, config: Config):
        children = []
        while len(children) < size - 1:
            parent2 = random.choice(parents)
            if random.random() < crossover_rate:
                child = self.cross(best_plan, parent2, config)
                if child is not None:
                    children.append(child)
        children.append(best_plan)
        return children

    def cross(self, plan1, plan2, config):
        if not self.valid_plans(plan1, plan2, config):
            return None

        groups = config.head_teachers.keys()
        child = SchoolPlan(groups)
        for name in groups:
            for day in list(Day):
                for hour in range(H_PER_DAY):
                    lesson = plan1.plans[name][day.value + hour] if plan1.fitness > plan2.fitness \
                        else plan2.plans[name][day.value + hour]
                    child.add_to_plan(config, name, day, hour, lesson)
        child.fill_plan(config)
        return child


class Generation:
    def __init__(self, config: Config, size=20, crossover_rate=0.7, mutation_rate=0.1, eval_criteria=None):
        self.CROSSOVER_RATE = crossover_rate
        self.MUTATION_RATE = mutation_rate
        self.EVAL_CRITERIA = eval_criteria  # TODO: set defaults and provide option

        self.gen_no = 0
        self.size = size
        self.config = config
        self.population = []
        for _ in range(size):
            plan = SchoolPlan(config.head_teachers.keys())
            plan.generate(config)
            # print(f"Generated plan: {plan}")
            self.population.append(plan)

    def evaluate(self):
        for plan in self.population:
            plan.evaluate(self.config)
            # print(f"Evaluated plan; fitness: {plan.fitness}")
        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def best_plan(self) -> SchoolPlan:
        return max(self.population, key=lambda x: x.fitness)

    def all(self):
        return [plan.as_dict() for plan in self.population]

    def statistics(self) -> dict:
        return {
            "max": self.best_plan().fitness,
            "avg": sum([plan.fitness for plan in self.population]) / self.size,
            "min": self.population[-1].fitness
        }

    def crossover(self, strategy: CrossoverStrategy = SinglePointCrossover()):
        # selection
        self.population.sort(key=lambda x: x.fitness)
        best_plan = self.best_plan()
        parents = self.population[: self.size // 2]

        # crossover
        self.population = strategy.crossover(parents, best_plan, self.size, self.CROSSOVER_RATE, self.config)
        self.gen_no += 1

    def mutate(self):
        for i in range(self.size - 1):
            if random.random() < self.MUTATION_RATE:
                self.population[i].swap(4)

    def purge_worst(self, min_limit: int):
        self.population = [plan for plan in self.population if plan.fitness > min_limit]
        purges = self.size - len(self.population)
        print(f"Purged {purges} worst plans")
        for _ in range(purges):
            plan = SchoolPlan(self.config.head_teachers.keys())
            plan.generate(self.config)
            self.population.append(plan)
