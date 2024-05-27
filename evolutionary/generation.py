import random
from abc import ABC

from evolutionary.config import Config, H_PER_DAY, Day
from evolutionary.school_plan import SchoolPlan


class CrossoverStrategy(ABC):
    def crossover(self, parents, best_plan, size, config: Config):
        pass

    def cross(self, plan1, plan2, config):
        pass

    def valid_plans(self, plan1: SchoolPlan, plan2: SchoolPlan, config: Config) -> bool:
        return plan1.plans.keys() == plan2.plans.keys() and plan1.plans.keys() == config.head_teachers.keys() \
            and plan1.plans != plan2.plans


class RouletteSinglePointCrossover(CrossoverStrategy):
    def crossover(self, parents, best_plan, size, config: Config):
        children = [best_plan]

        sum_fitness = sum([plan.fitness for plan in parents])
        probabilities = [plan.fitness / sum_fitness for plan in parents]
        while len(children) < size:
            parent1, parent2 = random.choices(parents, probabilities, k=2)
            if random.random() < config.cross_params["crossover_rate"]:
                child = self.cross(parent1, parent2, config)
                if child is not None:
                    children.append(child)
        return children

    def cross(self, plan1, plan2, config):
        if not self.valid_plans(plan1, plan2, config):
            return None

        div_factor = config.cross_params["div_factor"]

        groups = config.head_teachers.keys()
        child = SchoolPlan(groups)
        for name in groups:
            for day in list(Day):
                for hour in range(H_PER_DAY):
                    lesson = plan2.plans[name][day.value + hour] if random.random() < div_factor \
                        else plan1.plans[name][day.value + hour]
                    child.add_to_plan(config, name, day, hour, lesson)
        child.fill_plan(config)
        return child


class RouletteDayCrossover(CrossoverStrategy):
    def crossover(self, parents, best_plan, size, config: Config):
        children = [best_plan]

        sum_fitness = sum([plan.fitness for plan in parents])
        probabilities = [plan.fitness / sum_fitness for plan in parents]
        while len(children) < size:
            parent1, parent2 = random.choices(parents, probabilities, k=2)
            if random.random() < config.cross_params["crossover_rate"]:
                child = self.cross(parent1, parent2, config)
                if child is not None:
                    children.append(child)
        return children

    def cross(self, plan1, plan2, config):
        if not self.valid_plans(plan1, plan2, config):
            return None

        div_factor = config.cross_params["div_factor"]

        groups = config.head_teachers.keys()
        child = SchoolPlan(groups)
        for name in groups:
            for day in list(Day):
                plan = plan2 if random.random() < div_factor else plan1
                for hour in range(H_PER_DAY):
                    lesson = plan.plans[name][day.value + hour]
                    child.add_to_plan(config, name, day, hour, lesson)
        child.fill_plan(config)
        return child


class ChampionCrossover(CrossoverStrategy):
    def crossover(self, parents, best_plan, size, config: Config):
        children = [best_plan]
        while len(children) < size:
            parent2 = random.choice(parents)
            if random.random() < config.cross_params["crossover_rate"]:
                child = self.cross(best_plan, parent2, config)
                if child is not None:
                    children.append(child)
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
    def __init__(self, config: Config, purge=False):
        self.gen_no: int = 0
        self.size: int = config.population_size
        self.config: Config = config
        self.purge: bool = purge
        self.population: list = []
        for _ in range(self.size):
            plan = SchoolPlan(config.head_teachers.keys())
            plan.generate(config)
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

    def crossover(self, strategy: CrossoverStrategy = RouletteSinglePointCrossover()):
        # selection
        self.population.sort(key=lambda x: x.fitness)
        best_plan = self.best_plan()
        parents = self.population[: self.size // 2]

        # crossover
        self.population = strategy.crossover(parents, best_plan, self.size, self.config)
        self.gen_no += 1

        # purge worst plans
        if self.purge: # FIXME: this is not working
            self.purge_worst(0.4 * sum([plan.fitness for plan in self.population]) / self.size)

    def mutate(self):
        for i in range(self.size - 1):
            if random.random() < self.config.cross_params["mutation_rate"]:
                self.population[i].swap(4)

    def purge_worst(self, min_limit: float):
        self.population = [plan for plan in self.population if plan.fitness >= min_limit]
        purges = self.size - len(self.population)
        print(f"Purged {purges} worst plans")
        for _ in range(purges):
            plan = SchoolPlan(self.config.head_teachers.keys())
            plan.generate(self.config)
            self.population.append(plan)
