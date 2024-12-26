import time

from matplotlib import pyplot as plt

from evolutionary.config import MetaConfig, Config
from evolutionary.generation import Generation

NO_GENERATIONS = 1_000

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
    return stats

if __name__ == "__main__":
    mconfig = MetaConfig() # TODO: add config
    config = Config(mconfig)
    generation = Generation(config, mconfig)

    start = time.time()
    results = run_engine(generation)
    end = time.time()

    delta = end - start

    plot_graph(results, "test_1")

    print(f"Time spent in first example: {delta} seconds")
