import base64
import io
import os

import matplotlib.pyplot as plt
from flask import render_template, Flask, request

from data_manager import new_teacher_id, find_teacher, teacher_idx
from evolutionary.config import Config, MetaConfig
from evolutionary.generation import Generation
from evolutionary.selection import ChampionSelection, RouletteSelection
from state_manager import load_state, new_state, save_plans, save_config

templates_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
app = Flask(__name__, template_folder=templates_dir)

generation: Generation
config: Config
mconfig: MetaConfig
scores: list[dict]
generation, config, mconfig, scores = load_state()


def generate_graph():
    global scores
    x = [s[0] for s in scores]
    y_max = [s[1] for s in scores]
    y_avg = [s[2] for s in scores]
    y_min = [s[3] for s in scores]
    plt.figure(figsize=(10,5))
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

        if generation.gen_no % 25 == 0:
            stats = generation.statistics()
            scores.append((generation.gen_no, stats["max"], stats["avg"], stats["min"]))
            generation.evaluate()
    if generation.gen_no % 25 != 0:
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
        global mconfig, config
        teacher_name = request.form.get('t-name')
        print(teacher_name)
        mconfig.teachers.append({"id": new_teacher_id(mconfig), "name": teacher_name})
        mconfig.teachers.sort(key=lambda x: x["id"])

        save_config(mconfig)
        config = Config(mconfig)
        return render_template("teachers.html", teachers=mconfig.teachers)

@app.route('/teacher/<idx>', methods=['GET', 'PATCH', 'DELETE'])
def teacher_mod(idx):
    global mconfig, config
    if request.method == 'GET':
        teacher = find_teacher(idx, mconfig)
        if teacher is None:
            return render_template("teachers.html", teachers=mconfig.teachers)
        return render_template("teacher.html", teacher=teacher)
    if request.method == 'PATCH':
        teacher_name = request.form.get('t-name')
        teacher_id = teacher_idx(idx, mconfig)
        mconfig.teachers[teacher_id]["name"] = teacher_name
    if request.method == 'DELETE':
        teacher_id = teacher_idx(idx, mconfig)
        mconfig.teachers.pop(teacher_id)
    save_config(mconfig)
    config = Config(mconfig)
    return render_template("teachers.html", teachers=mconfig.teachers)


@app.route('/group/<name>', methods=['POST', 'DELETE'])
def group(name):
    global mconfig, config
    if request.method == 'POST':
        if name not in mconfig.subjects.keys():
            mconfig.subjects[name] = []
    else:
        if name in mconfig.subjects.keys():
            mconfig.subjects.pop(name)
    save_config(mconfig)
    config = Config(mconfig)
    return render_template("subjects.html", subjects=mconfig.subjects)


@app.route('/subjects', methods=['GET'])
def subjects():
    global mconfig
    return render_template("subjects.html", subjects=mconfig.subjects)


@app.route('/subject/<group>', methods=['GET', 'POST'])
def new_subject(group): # TODO
    if request.method == 'GET': # form
        return render_template("subject.html", group=group)
    else: # new
        pass


@app.route('/subject/<group>/<idx>', methods=['GET', 'PATCH', 'DELETE'])
def subject(group, idx): # TODO
    if request.method == 'GET':
        return render_template("subject.html", group=group)
    elif request.method == 'PATCH':
        pass
    else:
        pass


if __name__ == '__main__':
    app.run(debug=True, port=5000)
