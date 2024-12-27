import json
import time

from matplotlib import pyplot as plt

from evolutionary.config import MetaConfig, Config, EvaluationCriteria, CrossParams
from evolutionary.generation import Generation
from evolutionary.selection import RouletteSelection

NO_GENERATIONS = 1_000 # Number of generations algorithm should go through


def plot_graph(stats, file_name):
    x = [s["gen"] for s in stats]
    y_max = [s["max"] for s in stats]
    y_avg = [s["avg"] for s in stats]
    y_min = [s["min"] for s in stats]

    plt.figure(figsize=(10, 5))
    plt.plot(x, y_min, label='Min')
    plt.plot(x, y_avg, label='Avg')
    plt.plot(x, y_max, label='Max')
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
        gen.evaluate()

        if gen.gen_no % 50 == 0:
            stats.append(gen.statistics())
            print(gen.gen_no) # FIXME: delete when ok
    return stats


if __name__ == "__main__":
    # Loading 1st data set
    sf = open("test_sets/subjects_1.json", "r")
    tf = open("test_sets/teachers_1.json", "r")

    # Configuration for most "basic" algorithm
    mconfig = MetaConfig(
        population_size=100,
        selection=RouletteSelection(),
        teachers=json.load(tf),
        subjects=json.load(sf),
        eval_criteria=EvaluationCriteria(
            hours_weight=[1, 1, 1, 1, 1, 1, 1, 1],
            basic_importance=1,
            blank_lessons_importance=1,
            hours_per_day_importance=1,
            max_subject_hours_per_day_importance=1,
            subject_block_importance=1,
            teacher_block_importance=1,
            subject_at_end_or_start_importance=1,
        ),
        cross_params=CrossParams(
            crossover_rate=0.8,
            mutation_rate=0.01
        ),
        c=1.5
    )

    # Setup
    config = Config(mconfig)
    generation = Generation(config, mconfig)

    # Engine run
    start = time.time()
    results = run_engine(generation)
    end = time.time()

    delta = end - start

    # Results of test one
    plot_graph(results, "test_1")
    print(f"Time spent in first example: {delta} seconds")


def test2():
    # Loading 1st data set
    sf = open("test_sets/subjects_2.json", "r")
    tf = open("test_sets/teachers_2.json", "r")

    # Configuration with other selection method
    mconfig = MetaConfig(
        population_size=100,
        selection=RouletteSelection(),
        teachers=json.load(tf),
        subjects=json.load(sf),
        eval_criteria=EvaluationCriteria(
            hours_weight=[1, 1, 1, 1, 1, 1, 1, 1],
            basic_importance=1,
            blank_lessons_importance=1,
            hours_per_day_importance=1,
            max_subject_hours_per_day_importance=1,
            subject_block_importance=1,
            teacher_block_importance=1,
            subject_at_end_or_start_importance=1,
        ),
        cross_params=CrossParams(
            crossover_rate=0.8,
            mutation_rate=0.01
        ),
        k=4
    )
