from evolutionary.config import MetaConfig


def new_teacher_id(config: MetaConfig):
    idx = 1
    for t in config.teachers:
        if t["id"] == idx:
            idx += 1
        else:
            break
    return idx

def find_teacher(idx: int, config: MetaConfig):
    for t in config.teachers:
        if t["id"] == idx:
            return t
    return None

def teacher_idx(idx: int, config: MetaConfig):
    for i in range(len(config.teachers)):
        if config.teachers[i]["id"] == idx:
            return i
    return None

def teacher_occupied(teacher_id: int, mconfig: MetaConfig):
    for group in mconfig.subjects.values():
        for subject in group:
            if teacher_id == subject["teacher_id"]:
                return True
    return False

def new_subject_id(config: MetaConfig, group):
    idx = 1
    for s in config.subjects[group]:
        if s["id"] == idx:
            idx += 1
        else:
            break
    return idx

def find_subject(idx: int, config: MetaConfig, group):
    for s in config.subjects[group]:
        if s["id"] == idx:
            return s
    return None

def subject_idx(idx: int, config: MetaConfig, group):
    for i in range(len(config.subjects[group])):
        if config.subjects[group][i]["id"] == idx:
            return i
    return None
