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
    def __init__(self, crossover_rate: float = 0.8, mutation_rate: float = 0.01):
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
                 basic_importance: float = 1,
                 blank_lessons_importance: float = 1,
                 hours_per_day_importance: float = 1,
                 max_subject_hours_per_day_importance: float = 1,
                 subject_block_importance: float = 1,
                 teacher_block_importance: float = 1,
                 subject_at_end_or_start_importance: float = 1):
        if hours_weight is None:
            hours_weight = [1, 1, 1, 1, 1, 0.5, 0.1, -1]
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
                 selection,
                 s: int = 5,
                 elitism: bool = True,
                 population_size: int = 100,
                 eval_criteria: EvaluationCriteria = EvaluationCriteria(),
                 cross_params: CrossParams = CrossParams()):
        self.teachers: list = teachers
        self.subjects: dict = subjects
        self.elitism: bool = elitism
        self.population_size: int = population_size
        self.selection_strategy = selection
        self.eval: EvaluationCriteria = eval_criteria
        self.cross: CrossParams = cross_params
        self.S: int = s
        self.group_to_id = {i: group for i, group in enumerate(subjects.keys())}


class Config:
    def __init__(self, config: MetaConfig):
        self.no_groups: int = len(config.group_to_id.keys())
        self.elitism: bool = config.elitism
        self.population_size: int = config.population_size
        self.selection_strategy = config.selection_strategy
        self.eval = config.eval
        self.cross = config.cross
        self.S = config.S

        self.teachers: list = config.teachers
        self.subjects: list = [None] * self.no_groups
        for i in range(self.no_groups):
            self.subjects[i] = config.subjects[config.group_to_id[i]]
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
