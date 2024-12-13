import json

from evolutionary.config import MetaConfig, Config
from evolutionary.generation import Generation
from evolutionary.school_plan import SchoolPlan
from evolutionary.selection import RouletteSelection

DATA_DIR = "data"
SUBJECTS = "subjects.json"
TEACHERS = "teachers.json"
PLANS = "plans.json"
OTHER_CONFIG = "others.json"
STATS = "statistics.json"

def load_state() -> (Generation, Config, MetaConfig, list):
    mconfig = get_default_config()
    config = Config(mconfig)
    return (
        Generation(config, mconfig),
        config,
        mconfig,
        []
    )


def save_plans(population: list[SchoolPlan], stats: list):
    pf = open(DATA_DIR + PLANS, "w")
    stf = open(DATA_DIR + PLANS, "w")

    pf.write(json.dumps([pop.plans for pop in population]))
    stf.write(json.dumps(stats))


def load_plans() -> (list[SchoolPlan], list):
    pf = open(DATA_DIR + PLANS, "r")
    stf = open(DATA_DIR + PLANS, "r")

    plans = json.load(pf)

    return (
        [SchoolPlan(p) for p in plans],
        json.load(stf),
    )


def save_config(config: MetaConfig):
    sf = open(DATA_DIR + SUBJECTS, "w")
    tf = open(DATA_DIR + TEACHERS, "w")
    of = open(DATA_DIR + OTHER_CONFIG, "w")

    sf.write(json.dumps(config.subjects))
    tf.write(json.dumps(config.teachers))
    of.write(json.dumps({
        "size": config.population_size,
        "eval": config.eval,
        "cross": config.cross,
        "elitism": config.elitism,
        "selection": config.selection_strategy,
        "s": config.S
    }))


def load_config() -> MetaConfig:
    sf = open(DATA_DIR + SUBJECTS, "r")
    tf = open(DATA_DIR + TEACHERS, "r")
    of = open(DATA_DIR + OTHER_CONFIG, "r")

    other_config = json.load(of)

    return MetaConfig(
        population_size=other_config["size"],
        eval_criteria=other_config["eval"],
        cross_params=other_config["cross"],
        elitism=other_config["elitism"],
        selection=other_config["selection"],
        s=other_config["s"],
        teachers=json.load(tf),
        subjects=json.load(sf),
    )


def new_state() -> (Generation, Config, MetaConfig):
    mconfig = get_default_config()
    config = Config(mconfig)
    return Generation(config, mconfig), config, mconfig


def get_default_config() -> MetaConfig:
    sf = open(SUBJECTS, "r")
    tf = open(TEACHERS, "r")
    config = MetaConfig(
        population_size=100,
        selection=RouletteSelection(),
        teachers=json.load(tf),
        subjects=json.load(sf),
    )
    return config
