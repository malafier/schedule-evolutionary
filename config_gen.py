import json

from evolutionary.config import MetaConfig


def get_config() -> MetaConfig:
    sf = open("subjects.json", "r")
    tf = open("teachers.json", "r")
    config = MetaConfig(
        population_size=100,
        teachers=json.load(tf),
        subjects=json.load(sf),
    )
    return config
