import json

import evolutionary.crossover
import evolutionary.selection
from evolutionary.config import MetaConfig, Config, EvaluationCriteria, CrossParams
from evolutionary.generation import Generation
from evolutionary.school_plan import SchoolPlan

DATA_DIR = "data/"
SUBJECTS = "subjects.json"
TEACHERS = "teachers.json"
PLANS = "plans.json"
OTHER_CONFIG = "others.json"
STATS = "statistics.json"


def get_default_config() -> MetaConfig:
    sf = open(SUBJECTS, "r")
    tf = open(TEACHERS, "r")
    return MetaConfig(
        population_size=100,
        selection_strat=evolutionary.selection.RouletteSelection(),
        crossover_strat=evolutionary.crossover.Matrix2DStrategy(),
        c=2.0,
        k=5,
        teachers=json.load(tf),
        subjects=json.load(sf),
    )


def save_mconfig(mconfig: MetaConfig):
    sf = open(DATA_DIR + SUBJECTS, "w")
    tf = open(DATA_DIR + TEACHERS, "w")
    of = open(DATA_DIR + OTHER_CONFIG, "w")

    sf.write(json.dumps(mconfig.subjects))
    tf.write(json.dumps(mconfig.teachers))
    of.write(json.dumps({
        "size": mconfig.population_size,
        "eval": mconfig.eval.__dict__,
        "cross": mconfig.cross.__dict__,
        "elitism": mconfig.elitism,
        "selection_strat": mconfig.selection_strategy.__class__.__name__,
        "crossover_strat": mconfig.crossover_strategy.__class__.__name__,
        "c": mconfig.C,
        "k": mconfig.k
    }))


def load_mconfig() -> MetaConfig:
    try:
        sf = open(DATA_DIR + SUBJECTS, "r")
        tf = open(DATA_DIR + TEACHERS, "r")
        of = open(DATA_DIR + OTHER_CONFIG, "r")
    except FileNotFoundError:
        config = get_default_config()
        save_mconfig(config)
        return config

    other_config = json.load(of)

    return MetaConfig(
        population_size=other_config["size"],
        eval_criteria=EvaluationCriteria(
            hours_weight=other_config["eval"]["hours_weight"],
            basic_importance=other_config["eval"]["basic_imp"],
            blank_lessons_importance=other_config["eval"]["gap_imp"],
            hours_per_day_importance=other_config["eval"]["hpd_imp"],
            max_subject_hours_per_day_importance=other_config["eval"]["max_subj_hpd_imp"],
            subject_block_importance=other_config["eval"]["subj_block_imp"],
            teacher_block_importance=other_config["eval"]["teach_block_imp"],
            subject_at_end_or_start_importance=other_config["eval"]["subj_end_start_imp"],
        ),
        cross_params=CrossParams(
            crossover_rate=other_config["cross"]["crossover_rate"],
            mutation_rate=other_config["cross"]["mutation_rate"],
        ),
        elitism=other_config["elitism"],
        crossover_strat=evolutionary.crossover.str_to_class(other_config["crossover_strat"]),
        selection_strat=evolutionary.selection.str_to_class(other_config["selection_strat"]),
        c=other_config["c"],
        k=other_config["k"],
        teachers=json.load(tf),
        subjects=json.load(sf),
    )


def save_plans(generation: Generation, stats: list):
    pf = open(DATA_DIR + PLANS, "w")
    stf = open(DATA_DIR + STATS, "w")

    pf.write(json.dumps({
        "gen": generation.gen_no,
        "plans": [pop.plans for pop in generation.population]
    }))
    stf.write(json.dumps(stats))


def load_plans() -> (list[SchoolPlan], list, int):
    try:
        pf = open(DATA_DIR + PLANS, "r")
        stf = open(DATA_DIR + STATS, "r")
    except FileNotFoundError:
        mconfig = load_mconfig()
        gen = Generation(Config(mconfig), mconfig)
        save_plans(gen, [])
        return gen.population, [], 0

    content = json.load(pf)

    return (
        [SchoolPlan(len(p), p) for p in content["plans"]],
        json.load(stf),
        content["gen"]
    )


def load_state() -> (Generation, Config, MetaConfig, list):
    mconfig = load_mconfig()
    config = Config(mconfig)
    plans, stats, gen_no = load_plans()

    gen = Generation(config, mconfig, plans, gen_no)

    return (
        gen,
        config,
        mconfig,
        stats
    )


def new_state() -> (Generation, Config, MetaConfig):
    mconfig = load_mconfig()
    config = Config(mconfig)
    gen = Generation(config, mconfig)

    return gen, config, mconfig
