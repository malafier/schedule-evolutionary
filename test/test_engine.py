import json
import time

import numpy as np
from matplotlib import pyplot as plt

from evolutionary.config import MetaConfig, Config, EvaluationCriteria, CrossParams
from evolutionary.crossover import DoublePointCrossover, Matrix2DCrossover, UniformCrossover, SinglePointCrossover
from evolutionary.generation import Generation
from evolutionary.selection import RouletteSelection, TournamentSelection

NO_GENERATIONS = 1_000  # Number of generations algorithm should go through
SAMPLING_INTERVAL = 20

# Loading data sets
sf1 = open("test_sets/subjects_1.json", "r")
tf1 = open("test_sets/teachers_1.json", "r")
sf2 = open("test_sets/subjects_2.json", "r")
tf2 = open("test_sets/teachers_2.json", "r")
teachers1 = json.load(tf1)
subjects1 = json.load(sf1)
teachers2 = json.load(tf2)
subjects2 = json.load(sf2)

CONFIGS: list[MetaConfig] = [
    MetaConfig(
        population_size=100,
        elitism=True,
        selection_strat=RouletteSelection(),
        crossover_strat=SinglePointCrossover(),
        teachers=teachers1,
        subjects=subjects1,
        eval_criteria=EvaluationCriteria(),
        cross_params=CrossParams(
            crossover_rate=0.9,
            mutation_rate=0.15
        ),
        c=2.0
    ),
    MetaConfig(
        population_size=100,
        elitism=True,
        selection_strat=RouletteSelection(),
        crossover_strat=Matrix2DCrossover(),
        teachers=teachers2,
        subjects=subjects2,
        eval_criteria=EvaluationCriteria(),
        cross_params=CrossParams(
            crossover_rate=0.9,
            mutation_rate=0.15
        ),
        c=2.0
    ),
    MetaConfig(
        population_size=100,
        elitism=True,
        selection_strat=TournamentSelection(),
        crossover_strat=DoublePointCrossover(),
        teachers=teachers1,
        subjects=subjects1,
        eval_criteria=EvaluationCriteria(),
        cross_params=CrossParams(
            crossover_rate=0.8,
            mutation_rate=0.15
        ),
        k=10
    ),
    MetaConfig(
        population_size=100,
        elitism=True,
        selection_strat=TournamentSelection(),
        crossover_strat=UniformCrossover(),
        teachers=teachers2,
        subjects=subjects2,
        eval_criteria=EvaluationCriteria(),
        cross_params=CrossParams(
            crossover_rate=0.8,
            mutation_rate=0.15
        ),
        k=10
    ),
]


def plot_graph(stats, file_name):
    x = [s["gen"] for s in stats]
    y_max = [s["max"] for s in stats]
    y_avg = [s["avg"] for s in stats]
    y_min = [s["min"] for s in stats]
    m, b = np.polyfit(x, y_avg, deg=1)
    y_lin = [m * x_i + b for x_i in x]

    plt.figure(figsize=(10, 5))
    plt.plot(x, y_min, label='Min')
    plt.plot(x, y_avg, label='Avg')
    plt.plot(x, y_max, label='Max')
    plt.plot(x, y_lin, label='Lin', linestyle='--')
    plt.ylabel('Przystosowanie')
    plt.xlabel('Generacje')
    plt.legend()
    plt.title('Przystosowanie przez generacje')

    plt.savefig(file_name + ".png", bbox_inches="tight")


def run_engine(gen: Generation) -> list[dict]:
    stats = []
    gen.evaluate()
    for i in range(NO_GENERATIONS):
        gen.next_gen()
        gen.fix()
        gen.evaluate()

        if gen.gen_no % SAMPLING_INTERVAL == 0:
            stats.append(gen.statistics())
    return stats


if __name__ == "__main__":
    for i, mconfig in enumerate(CONFIGS):
        # Setup
        config = Config(mconfig)
        generation = Generation(config, mconfig)

        # Running engine
        start = time.time()
        results = run_engine(generation)
        end = time.time()

        delta = round(end - start, 4)

        # Results of test
        plot_graph(results, f"test_{i + 1}")
        print(f"Time spent on test {i + 1}: {delta} seconds")
