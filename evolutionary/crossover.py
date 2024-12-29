from abc import ABC

from evolutionary.crossover_alg import matrix_crossover, single_point_crossover, double_point_crossover, \
    uniform_crossover
from evolutionary.school_plan import SchoolPlan


class CrossoverStrategy(ABC):
    def cross(self, parent1: SchoolPlan, parent2: SchoolPlan, no_groups: int) -> (SchoolPlan, SchoolPlan):
        pass

    def __name__(self):
        pass

    def __str__(self):
        pass


class Matrix2DStrategy(CrossoverStrategy):
    def cross(self, parent1: SchoolPlan, parent2: SchoolPlan, no_groups: int) -> (SchoolPlan, SchoolPlan):
        return matrix_crossover(parent1, parent2, no_groups)

    def __name__(self):
        return "Matrix2DStrategy"

    def __str__(self):
        return "Matrix2DStrategy"


class SinglePointStrategy(CrossoverStrategy):
    def cross(self, parent1: SchoolPlan, parent2: SchoolPlan, no_groups: int) -> (SchoolPlan, SchoolPlan):
        return single_point_crossover(parent1, parent2, no_groups)

    def __name__(self):
        return "SinglePointStrategy"

    def __str__(self):
        return "SinglePointStrategy"


class DoublePointStrategy(CrossoverStrategy):
    def cross(self, parent1: SchoolPlan, parent2: SchoolPlan, no_groups: int) -> (SchoolPlan, SchoolPlan):
        return double_point_crossover(parent1, parent2, no_groups)

    def __name__(self):
        return "DoublePointStrategy"

    def __str__(self):
        return "DoublePointStrategy"


class UniformStrategy(CrossoverStrategy):
    def cross(self, parent1: SchoolPlan, parent2: SchoolPlan, no_groups: int) -> (SchoolPlan, SchoolPlan):
        return uniform_crossover(parent1, parent2, no_groups)

    def __name__(self):
        return "UniformStrategy"

    def __str__(self):
        return "UniformStrategy"
