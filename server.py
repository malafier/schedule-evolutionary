import base64
import io
import os
import time

import matplotlib.pyplot as plt
from flask import render_template, Flask, request

from evolutionary.config import Config
from evolutionary.generation import Generation, ChampionCrossover, RouletteSinglePointCrossover, RouletteDayCrossover
from main import get_config

templates_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
app = Flask(__name__, template_folder=templates_dir)

generation: Generation | None = None
config: Config | None = None
crossover_strategy = ChampionCrossover()
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


@app.after_request
def add_cache_control_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/', methods=['GET'])
def get_school_plan():
    global generation, scores, config
    scores = []
    config = get_config()
    generation = Generation(config)
    generation.evaluate()
    stats = generation.statistics()
    scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))

    print(config.eval_criteria)
    return render_template(
        "main.html",
        score=scores[-1],
        config=config,
        selection=crossover_strategy.__class__.__name__
    )


@app.route('/nextgen', methods=['GET'])
def make_next_generation():
    global generation, scores
    generation.evaluate()
    generation.crossover(crossover_strategy)
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
        generation.evaluate()
        generation.crossover(crossover_strategy)
        generation.mutate()
        generation.evaluate()
    stats = generation.statistics()
    scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))

    graph = generate_graph()
    return render_template("statistics.html", score=scores[-1], graph=graph)

# global time_eval, time_cross, time_mut
@app.route('/next50gen', methods=['GET'])
def make_next_50_gens():
    global generation, scores
    # global time_eval, time_cross, time_mut
    # times = [0, 0, 0]
    # time_eval > time_cross >> time_mut
    for i in range(50):
        # time_start = time.time()
        generation.evaluate()
        # time_eval = time.time() - time_start
        generation.crossover(crossover_strategy)
        # time_cross = time.time() - time_eval
        generation.mutate()
        # time_mut = time.time() - time_cross
        generation.evaluate()
        # times[0] += time_eval
        # times[1] += time_cross
        # times[2] += time_mut
    # print("Evaluation time: ", times[0], "Crossover time: ", times[1], "Mutation time: ", times[2])
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


@app.route('/config', methods=['GET'])  # TODO: finalise
def alter_configuration():
    global generation, config, scores, crossover_strategy

    config.population_size = int(request.form.get('population'))
    config.elitism = request.form.get('elitism') == 'on'
    config.cross_params['crossover_rate'] = float(request.form.get('crossover'))
    config.cross_params['div_factor'] = float(request.form.get('div_factor'))
    config.cross_params['mutation_rate'] = float(request.form.get('mutation'))

    crossover_strategy = RouletteSinglePointCrossover() \
        if request.form.get('crossover_strategy') == 'roulette_l' else ChampionCrossover()
    crossover_strategy = RouletteDayCrossover() \
        if request.form.get('crossover_strategy') == 'roulette_d' else crossover_strategy

    config.eval_criteria['importance']['basic_evaluation'] = float(request.form.get('imp_basic'))
    config.eval_criteria['importance']['blank_lessons_evaluation'] = float(request.form.get('imp_blank'))
    config.eval_criteria['importance']['hours_per_day_evaluation'] = float(request.form.get('imp_hours_per_day'))
    config.eval_criteria['importance']['subject_block_evaluation'] = float(request.form.get('imp_lesson_block'))
    config.eval_criteria['importance']['teacher_block_evaluation'] = float(request.form.get('imp_teacher_block'))
    config.eval_criteria['importance']['subject_at_end_or_start_evaluation'] = \
        float(request.form.get('imp_start_end_day_subject'))

    generation = Generation(config)
    generation.evaluate()
    scores.clear()
    stats = generation.statistics()
    scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))

    return render_template(
        "config_input.html",
        config=config,
        selection=crossover_strategy.__class__.__name__
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
