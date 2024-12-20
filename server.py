import base64
import io
import os

import matplotlib.pyplot as plt
from flask import render_template, Flask, request

from evolutionary.config import Config
from evolutionary.generation import Generation
from evolutionary.selection import ChampionSelection, RouletteSelection
from state_manager import load_state, new_state, save_plans

templates_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
app = Flask(__name__, template_folder=templates_dir)

generation, config, mconfig, scores = load_state()


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

    if generation.gen_no == 0:
        generation.evaluate()
        stats = generation.statistics()
        scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))

    if len(scores) > 1:
        graph = generate_graph()
    else:
        graph = None

    return render_template(
        "main.html",
        score=scores[-1],
        config=config,
        graph=graph
    )

@app.route('/new-plan', methods=['GET'])
def regenerate_plan():
    global generation, scores, config, mconfig

    generation, config, mconfig = new_state()
    scores = []

    generation.evaluate()
    stats = generation.statistics()
    scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))

    save_plans(generation, stats)
    return render_template("statistics.html", score=scores[-1])

@app.route('/next-gens', methods=['POST'])
def next_n_gens():
    global generation, scores

    generation.evaluate()

    n = int(request.form.get('n'))
    for i in range(n):
        generation.next_gen()
        generation.evaluate()

        if generation.gen_no % 20 == 0:
            stats = generation.statistics()
            scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))
            generation.evaluate()
    stats = generation.statistics()
    scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))

    graph = generate_graph()
    save_plans(generation, scores)
    return render_template("statistics.html", score=scores[-1], graph=graph)


@app.route('/all', methods=['GET'])
def show_all_plans():
    global generation
    return render_template("teachers_plans.html", school_plans=generation.all(), config=generation.meta)


@app.route('/best-plan', methods=['GET'])
def show_plan():
    global generation
    school_plan: dict = generation.best_plan().as_dict(generation.config, generation.meta)

    return render_template("plan.html", school_plan=school_plan, config=generation.meta)


@app.route('/config', methods=['POST'])
def alter_configuration():
    global generation, mconfig, config, scores

    mconfig.population_size = int(request.form.get('population_size'))
    mconfig.elitism = request.form.get('elitism') == 'on'
    mconfig.cross\
        .crossover(float(request.form.get('crossover')))\
        .mutation(float(request.form.get('mutation')))

    mconfig.selection_strategy = RouletteSelection() \
        if request.form.get('selection_strategy') == 'roulette' else ChampionSelection()

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

    return render_template("config_input.html", config=config)


@app.route('/teachers-plans', methods=['GET'])
def teacher_plans():
    global generation, config
    return render_template(
        "teachers_plans.html",
        t_plans=generation.best_plan().teachers_plans(config),
        config=config
    )


@app.route('/teachers', methods=['GET'])
def teachers():
    global mconfig
    return render_template("teachers.html", teachers=mconfig.teachers)


@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    if request.method == 'GET':
        return render_template("teacher.html")
    else:
        pass


@app.route('/subjects', methods=['GET'])
def subjects():
    global mconfig
    return render_template("subjects.html", subjects=mconfig.subjects)


@app.route('/subject', methods=['GET', 'POST'])
def subject():
    if request.method == 'GET':
        return render_template("subject.html")
    else:
        pass


if __name__ == '__main__':
    app.run(debug=True, port=5000)
