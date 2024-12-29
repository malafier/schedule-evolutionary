import base64
import io
import os

import matplotlib.pyplot as plt
from flask import render_template, Flask, request

import state_io
from evolutionary.config import Config, MetaConfig
from evolutionary.generation import Generation
from evolutionary.selection import TournamentSelection, RouletteSelection

templates_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
app = Flask(__name__, template_folder=templates_dir)

SAMPLING_INTERVAL = 20

generation: Generation
config: Config
mconfig: MetaConfig
scores: list
generation, config, mconfig, scores = state_io.load_state()


def generate_graph():
    global scores
    x = [s["gen"] for s in scores]
    y_max = [s["max"] for s in scores]
    y_avg = [s["avg"] for s in scores]
    y_min = [s["min"] for s in scores]
    plt.figure(figsize=(10, 5))
    plt.plot(x, y_min, label='Min')
    plt.plot(x, y_avg, label='Avg')
    plt.plot(x, y_max, label='Max')
    plt.ylabel('Przystosowanie')
    plt.xlabel('Generacje')
    plt.legend()
    plt.title('Przystosowanie przez generacje')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.clf()

    return 'data:image/png;base64,{}'.format(plot_url)


def reset_and_save_config():
    global mconfig, config, generation, scores
    del config
    config = Config(mconfig)
    state_io.save_mconfig(mconfig)

    generation = Generation(config, mconfig)
    generation.evaluate()
    scores = [generation.statistics()]

    state_io.save_plans(generation, scores)


@app.after_request
def add_cache_control_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/', methods=['GET'])
def get_school_plan():
    global generation, scores, config

    if generation.gen_no == 0 and len(scores) < 1:
        generation.evaluate()
        scores.append(generation.statistics())
        state_io.save_plans(generation, scores)

    graph = generate_graph() if len(scores) > 1 else None

    return render_template(
        "main.html",
        score=scores[-1],
        config=config,
        graph=graph
    )


@app.route('/new-plan', methods=['GET'])
def regenerate_plan():
    global generation, scores, config, mconfig

    generation, config, mconfig = state_io.new_state()
    scores = []

    generation.evaluate()
    scores.append(generation.statistics())

    state_io.save_plans(generation, scores)
    return render_template("statistics.html", score=scores[-1])


@app.route('/next-gens', methods=['POST'])
def next_gens():
    global generation, scores

    generation.evaluate()

    n = int(request.form.get('n'))
    for i in range(n):
        generation.next_gen()
        generation.fix()
        generation.evaluate()

        if generation.gen_no % SAMPLING_INTERVAL == 0:
            scores.append(generation.statistics())
    if generation.gen_no % SAMPLING_INTERVAL != 0:
        generation.evaluate()
        scores.append(generation.statistics())

    graph = generate_graph()
    state_io.save_plans(generation, scores)
    return render_template("statistics.html", score=scores[-1], graph=graph)


@app.route('/best-plan', methods=['GET'])
def show_plan():
    global generation
    school_plan: dict = generation.best_plan().as_dict(generation.config, generation.meta)

    return render_template("plan.html", school_plan=school_plan, config=generation.meta)


@app.route('/compact-plan', methods=['GET'])
def show_compact_plan():
    global generation
    school_plan: dict = generation.best_plan().as_dict(generation.config, generation.meta)

    return render_template("compact_plan.html", school_plan=school_plan, config=generation.meta)


@app.route('/config', methods=['PATCH'])
def alter_configuration():
    global generation, mconfig, config, scores

    mconfig.population_size = int(request.form.get('population_size'))
    mconfig.elitism = request.form.get('elitism') == 'on'
    mconfig.cross \
        .crossover(float(request.form.get('crossover'))) \
        .mutation(float(request.form.get('mutation')))

    mconfig.selection_strategy = RouletteSelection() \
        if request.form.get('selection_strategy') == 'roulette' else TournamentSelection()

    mconfig.C = float(request.form.get("c"))
    mconfig.k = int(request.form.get("k"))

    mconfig.eval \
        .basic_importance(float(request.form.get('imp_basic'))) \
        .gap_period_importance(float(request.form.get('imp_gap'))) \
        .hours_per_day_importance(float(request.form.get('imp_hours_per_day'))) \
        .max_subject_hours_per_day_importance(float(request.form.get('imp_max_hours_per_day'))) \
        .subject_block_importance(float(request.form.get('imp_lesson_block'))) \
        .teacher_block_importance(float(request.form.get('imp_teacher_block'))) \
        .subject_at_end_or_start_importance(float(request.form.get('imp_start_end_day_subject')))

    for i in range(8):
        mconfig.eval.hours_weight[i] = float(request.form.get(str(i)))

    config = Config(mconfig)
    generation = Generation(config, mconfig)
    generation.evaluate()
    scores = [generation.statistics()]

    state_io.save_mconfig(mconfig)
    state_io.save_plans(generation, scores)
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
        return render_template("forms/new_teacher.html")
    else:
        global mconfig, config
        teacher_name = request.form.get('t-name')
        mconfig.new_teacher(teacher_name)

        reset_and_save_config()
        return render_template("teachers.html", teachers=mconfig.teachers)


@app.route('/teacher/<idx>', methods=['GET', 'PATCH', 'DELETE'])
def teacher_mod(idx):
    global mconfig, config
    idx = int(idx)

    if request.method == 'GET':
        teacher = mconfig.find_teacher(idx)
        if teacher is None:
            return render_template("teachers.html", teachers=mconfig.teachers)
        return render_template("forms/edit_teacher.html", teacher=teacher)
    if request.method == 'PATCH':
        teacher_name = request.form.get('t-name')
        mconfig.update_teacher(idx, teacher_name)
    if request.method == 'DELETE':
        if mconfig.teacher_occupied(idx):
            return render_template("teachers.html", teachers=mconfig.teachers)
        mconfig.delete_teacher(idx)

    reset_and_save_config()
    return render_template("teachers.html", teachers=mconfig.teachers)


@app.route('/group', methods=['POST'])
def add_group():
    global mconfig, config
    group_name = request.form.get('g-name')
    if group_name not in mconfig.subjects.keys():
        mconfig.subjects[group_name] = []

    reset_and_save_config()
    return render_template("subjects.html", subjects=mconfig.subjects)


@app.route('/group/<name>', methods=['DELETE'])
def delete_group(name):
    global mconfig, config
    if name in mconfig.subjects.keys():
        mconfig.subjects.pop(name)

    reset_and_save_config()
    return render_template("subjects.html", subjects=mconfig.subjects)


@app.route('/subjects', methods=['GET'])
def subjects():
    global mconfig
    return render_template("subjects.html", subjects=mconfig.subjects)


@app.route('/subject/<group>', methods=['GET', 'POST'])
def new_subject(group):
    global mconfig, config
    if request.method == 'GET':
        return render_template("forms/new_subject.html", group=group, teachers=mconfig.teachers)
    else:
        subject_name = request.form.get('s-name')
        subject_hours = int(request.form.get('s-hours'))
        subject_teacher = int(request.form.get('s-teacher'))
        subject_start_end = request.form.get('s-sted') == "on"

        mconfig.new_subject(
            group,
            subject_name=subject_name,
            subject_hours=subject_hours,
            subject_teacher=subject_teacher,
            subject_start_end=subject_start_end
        )

        reset_and_save_config()
        return render_template("subjects.html", subjects=mconfig.subjects)


@app.route('/subject/<group>/<idx>', methods=['GET', 'PATCH', 'DELETE'])
def subject(group, idx):
    global mconfig, config
    idx = int(idx)

    if request.method == 'GET':
        subject = mconfig.find_subject(idx, group)
        return render_template(
            "forms/edit_subject.html",
            group=group,
            subject=subject,
            teachers=mconfig.teachers
        )
    elif request.method == 'PATCH':
        subject_name = request.form.get('s-name')
        subject_hours = int(request.form.get('s-hours'))
        subject_teacher = int(request.form.get('s-teacher'))
        subject_start_end = request.form.get('s-sted') == "on"

        mconfig.update_subject(
            group,
            idx,
            subject_name=subject_name,
            subject_hours=subject_hours,
            subject_teacher=subject_teacher,
            subject_start_end=subject_start_end
        )
    else:
        mconfig.delete_subject(group, idx)

    reset_and_save_config()
    return render_template("subjects.html", subjects=mconfig.subjects)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
