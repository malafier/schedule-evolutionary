from evolutionary.config import MetaConfig


def new_teacher_id(config: MetaConfig):
    idx = 1
    for t in config.teachers:
        if t["id"] == idx:
            idx += 1
        else:
            break
    return idx

def find_teacher(idx, config: MetaConfig):
    for t in config.teachers:
        if t["id"] == idx:
            return t
    return None

def teacher_idx(idx, config: MetaConfig):
    for i in range(len(config.teachers)):
        if config.teachers[i]["id"] == idx:
            return i
    return None