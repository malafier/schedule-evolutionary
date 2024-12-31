from enum import Enum

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
H_PER_DAY = 8


class Day(Enum):
    MON = 0 * H_PER_DAY
    TUE = 1 * H_PER_DAY
    WED = 2 * H_PER_DAY
    THU = 3 * H_PER_DAY
    FRI = 4 * H_PER_DAY


class CrossParams:
    def __init__(self, crossover_rate: float = 0.8, mutation_rate: float = 0.1):
        self.crossover_rate: float = crossover_rate
        self.mutation_rate: float = mutation_rate

    def crossover(self, rate: float):
        self.crossover_rate = rate
        return self

    def mutation(self, rate: float):
        self.mutation_rate = rate
        return self


class EvaluationCriteria:
    def __init__(self,
                 hours_weight=None,
                 basic_importance: float = 1.0,
                 blank_lessons_importance: float = 1.0,
                 hours_per_day_importance: float = 1.0,
                 max_subject_hours_per_day_importance: float = 1.0,
                 subject_block_importance: float = 1.0,
                 teacher_block_importance: float = 1.0,
                 subject_at_end_or_start_importance: float = 1.0):
        if hours_weight is None:
            hours_weight = [1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.1, -1.0]
        self.hours_weight: list = hours_weight
        self.basic_imp: float = basic_importance
        self.gap_imp: float = blank_lessons_importance
        self.hpd_imp: float = hours_per_day_importance
        self.max_subj_hpd_imp: float = max_subject_hours_per_day_importance
        self.subj_block_imp: float = subject_block_importance
        self.teach_block_imp: float = teacher_block_importance
        self.subj_end_start_imp: float = subject_at_end_or_start_importance

    def hours_weights(self, weights: list):
        self.hours_weight = weights
        return self

    def basic_importance(self, importance: float):
        self.basic_imp = importance
        return self

    def gap_period_importance(self, importance: float):
        self.gap_imp = importance
        return self

    def hours_per_day_importance(self, importance: float):
        self.hpd_imp = importance
        return self

    def max_subject_hours_per_day_importance(self, importance: float):
        self.max_subj_hpd_imp = importance
        return self

    def subject_block_importance(self, importance: float):
        self.subj_block_imp = importance
        return self

    def teacher_block_importance(self, importance: float):
        self.teach_block_imp = importance
        return self

    def subject_at_end_or_start_importance(self, importance: float):
        self.subj_end_start_imp = importance
        return self


class MetaConfig:
    def __init__(self,
                 teachers: list,
                 subjects: dict,
                 selection_strat,
                 crossover_strat,
                 c: float = 2.0,
                 k: int = 5,
                 elitism: bool = True,
                 population_size: int = 100,
                 eval_criteria: EvaluationCriteria = EvaluationCriteria(),
                 cross_params: CrossParams = CrossParams()):
        self.teachers: list[dict] = teachers
        self.subjects: dict = subjects
        self.elitism: bool = elitism
        self.population_size: int = population_size
        self.selection_strategy = selection_strat
        self.crossover_strategy = crossover_strat
        self.eval: EvaluationCriteria = eval_criteria
        self.cross: CrossParams = cross_params
        self.C: float = c
        self.k: int = k

    def new_teacher(self, name: str):
        idx = 1
        for t in self.teachers:
            if t["id"] == idx:
                idx += 1
            else:
                break

        self.teachers.append({"id": idx, "name": name})
        self.teachers.sort(key=lambda x: x["id"])

    def find_teacher(self, idx: int):
        for t in self.teachers:
            if t["id"] == idx:
                return t
        return None

    def update_teacher(self, idx: int, name: str):
        for i in range(len(self.teachers)):
            if self.teachers[i]["id"] == idx:
                self.teachers[i]["name"] = name
                return

    def delete_teacher(self, idx: int):
        for i in range(len(self.teachers)):
            if self.teachers[i]["id"] == idx:
                self.teachers.pop(i)
                return

    def teacher_occupied(self, teacher_id: int):
        for group in self.subjects.values():
            for subject in group:
                if teacher_id == subject["teacher_id"]:
                    return True
        return False

    def new_subject(self, group: str, **kwargs):
        idx = 1
        for s in self.subjects[group]:
            if s["id"] == idx:
                idx += 1
            else:
                break

        self.subjects[group].append({
            "id": idx,
            "name": kwargs["subject_name"],
            "hours": kwargs["subject_hours"],
            "teacher_id": kwargs["subject_teacher"],
            "start_end": kwargs["subject_start_end"]
        })
        self.subjects[group].sort(key=lambda x: x["id"])

    def find_subject(self, idx: int, group: str):
        for s in self.subjects[group]:
            if s["id"] == idx:
                return s
        return None

    def update_subject(self, group: str, subject_id: int, **kwargs):
        for i in range(len(self.subjects[group])):
            if self.subjects[group][i]["id"] == subject_id:
                self.subjects[group][i]["name"] = kwargs["subject_name"]
                self.subjects[group][i]["hours"] = kwargs["subject_hours"]
                self.subjects[group][i]["teacher_id"] = kwargs["subject_teacher"]
                self.subjects[group][i]["start_end"] = kwargs["subject_start_end"]
                self.subjects[group].sort(key=lambda x: x["id"])
                return

    def delete_subject(self, group: str, idx: int):
        for i in range(len(self.subjects[group])):
            if self.subjects[group][i]["id"] == idx:
                self.subjects[group].pop(i)
                return


class Config:
    def __init__(self, mconfig: MetaConfig):
        self.no_groups: int = len(mconfig.subjects)
        self.elitism: bool = mconfig.elitism
        self.population_size: int = mconfig.population_size
        self.eval = mconfig.eval
        self.cross = mconfig.cross
        self.k = mconfig.k
        self.C = mconfig.C

        self.group_to_id = {i: group for i, group in enumerate(mconfig.subjects.keys())}
        self.teachers: list = mconfig.teachers
        self.subjects: list = [None] * self.no_groups
        for i in range(self.no_groups):
            self.subjects[i] = mconfig.subjects[self.group_to_id[i]]
        self.sub_to_teach: list = [None] * self.no_groups
        for i in range(self.no_groups):
            self.sub_to_teach[i] = {subject["id"]: subject["teacher_id"] for subject in self.subjects[i]}

    def hours_by_id(self, group_id: int, subject_id: int) -> int:
        for subject in self.subjects[group_id]:
            if subject["id"] == subject_id:
                return subject["hours"]
        return -1

    def teacher_by_subject(self, group_id: int, subject_id: int) -> int:
        for subject in self.subjects[group_id]:
            if subject["id"] == subject_id:
                return subject["teacher_id"]
        return -1
