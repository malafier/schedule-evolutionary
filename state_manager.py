import json

from evolutionary.config import MetaConfig, Config
from evolutionary.generation import Generation
from evolutionary.selection import RouletteSelection


def load_state() -> (Generation, Config, MetaConfig, list):
    mconfig = get_default_config()
    config = Config(mconfig)
    return (
        Generation(config, mconfig),
        config,
        mconfig,
        []
    )

def new_state() -> (Generation, Config, MetaConfig):
    mconfig = get_default_config()
    config = Config(mconfig)
    return Generation(config, mconfig), config, mconfig

def get_default_config() -> MetaConfig:
    sf = open("subjects.json", "r")
    tf = open("teachers.json", "r")
    config = MetaConfig(
        population_size=100,
        selection=RouletteSelection(),
        teachers=json.load(tf),
        subjects=json.load(sf),
    )
    return config
