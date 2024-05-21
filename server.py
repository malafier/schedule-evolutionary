import os
import io
import base64
import time

from flask import render_template, Flask
import matplotlib.pyplot as plt

from evolutionary.generation import Generation, ChampionCrossover
from main import get_generation

templates_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
app = Flask(__name__, template_folder=templates_dir)

generation: Generation | None = None
scores = []
plans = []  # TODO: Add plans


def generate_graph():
    global scores
    x = [s[0] for s in scores]
    y_max = [s[1] for s in scores]
    y_avg = [s[2] for s in scores]
    y_min = [s[3] for s in scores]
    plt.plot(x, y_min, label='Min')
    plt.plot(x, y_avg, label='Avg')
    plt.plot(x, y_max, label='Max')
    plt.ylabel('Score')
    plt.xlabel('Generation')
    plt.legend()
    plt.title('Scores over generations')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.clf()

    return 'data:image/png;base64,{}'.format(plot_url)


@app.route('/', methods=['GET'])
def get_school_plan():
    global generation, scores
    scores = []
    generation = get_generation()
    generation.evaluate()
    stats = generation.statistics()
    scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))
    return render_template("main.html", score=scores[-1])


@app.route('/nextgen', methods=['GET'])
def make_next_generation():
    global generation, scores
    # generation.purge_worst(scores[-1][2] - (scores[-1][2]-scores[-1][3] * 0.8))
    generation.evaluate()
    generation.crossover(ChampionCrossover())
    generation.mutate()
    generation.evaluate()
    stats = generation.statistics()
    scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))

    graph = generate_graph()
    return render_template("statistics.html", score=scores[-1], graph=graph)


@app.route('/next10gen', methods=['GET'])
def make_next_10_gens():
    global generation, scores
    # time_eval > time_cross >> time_mut
    for i in range(10):
        # generation.purge_worst(scores[-1][2] - (scores[-1][2]-scores[-1][3] * 0.8))
        generation.evaluate()
        generation.crossover(ChampionCrossover())
        generation.mutate()
        generation.evaluate()
    stats = generation.statistics()
    scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))

    graph = generate_graph()
    return render_template("statistics.html", score=scores[-1], graph=graph)


@app.route('/next50gen', methods=['GET'])
def make_next_50_gens():
    global generation, scores
    # time_eval > time_cross >> time_mut
    for i in range(50):
        # generation.purge_worst(scores[-1][2] - (scores[-1][2]-scores[-1][3] * 0.8))
        generation.evaluate()
        generation.crossover(ChampionCrossover())
        generation.mutate()
        generation.evaluate()
    stats = generation.statistics()
    scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))

    graph = generate_graph()
    return render_template("statistics.html", score=scores[-1], graph=graph)


@app.route('/all', methods=['GET'])
def show_all_plans():
    global generation
    return render_template("all_plans.html", school_plans=generation.all(), config=generation.config)


@app.route('/best-plan', methods=['GET'])
def show_plan():
    global generation
    school_plan: dict = generation.best_plan().as_dict()
    return render_template("plan.html", school_plan=school_plan, config=generation.config)


# @app.route('/genomes', methods=['GET'])
# def show_genomes():
#     global generation
#     return render_template("genomes.html", genomes=generation.genomes())


if __name__ == '__main__':
    app.run(debug=True, port=5000)
