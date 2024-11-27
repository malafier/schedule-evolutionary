import base64
import io
import os

import matplotlib.pyplot as plt
from flask import render_template, Flask, request

from evolutionary.config import Config, MetaConfig
from evolutionary.generation import Generation, ChampionSelection, RouletteSinglePointSelection
from config_gen import get_config

templates_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
app = Flask(__name__, template_folder=templates_dir)

generation: Generation | None = None
config: Config | None = None
mconfig: MetaConfig | None = None
selection_strategy = ChampionSelection()
scores = []


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
    global generation, scores, config, mconfig
    scores = []
    mconfig = get_config()
    config = Config(mconfig)

    generation = Generation(config, mconfig)
    generation.evaluate()

    stats = generation.statistics()
    scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))

    return render_template(
        "main.html",
        score=scores[-1],
        config=config,
        selection=selection_strategy.__class__.__name__
    )


@app.route('/next-n-gen', methods=['POST'])
def make_next_n_gens():
    global generation, scores

    n = int(request.form.get('n'))
    for i in range(n):
        generation.selection_crossover(selection_strategy)
        # generation.mutate()
        generation.evaluate()

        if generation.gen_no % 20 == 0:
            stats = generation.statistics()
            scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))
    stats = generation.statistics()
    scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))

    graph = generate_graph()
    return render_template("statistics.html", score=scores[-1], graph=graph)


@app.route('/all', methods=['GET'])
def show_all_plans():
    global generation
    return render_template("all_plans.html", school_plans=generation.all(), config=generation.meta)


@app.route('/best-plan', methods=['GET'])
def show_plan():
    global generation
    school_plan: dict = generation.best_plan().as_dict(generation.config, generation.meta)
    return render_template("plan.html", school_plan=school_plan, config=generation.meta)


@app.route('/config', methods=['POST'])
def alter_configuration():
    global generation, mconfig, config, scores, selection_strategy

    mconfig.population_size = int(request.form.get('population_size'))
    mconfig.elitism = request.form.get('elitism') == 'on'
    mconfig.cross\
        .crossover(float(request.form.get('crossover')))\
        .mutation(float(request.form.get('mutation')))

    selection_strategy = RouletteSinglePointSelection() \
        if request.form.get('crossover_strategy') == 'roulette_l' else ChampionSelection()

    mconfig.eval\
        .basic_importance(float(request.form.get('imp_basic')))\
        .gap_period_importance(float(request.form.get('imp_gap')))\
        .hours_per_day_importance(float(request.form.get('imp_hours_per_day')))\
        .max_subject_hours_per_day_importance(float(request.form.get('imp_max_hours_per_day')))\
        .subject_block_importance(float(request.form.get('imp_lesson_block')))\
        .teacher_block_importance(float(request.form.get('imp_teacher_block')))\
        .subject_at_end_or_start_importance(float(request.form.get('imp_start_end_day_subject')))

    config = Config(mconfig)
    generation = Generation(config, mconfig)
    generation.evaluate()
    scores.clear()
    stats = generation.statistics()
    scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))

    return render_template(
        "config_input.html",
        config=config,
        selection=selection_strategy.__class__.__name__
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
