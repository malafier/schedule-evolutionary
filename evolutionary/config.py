from enum import Enum

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
H_PER_DAY = 8
DEFAULT_EVAL_CRITERIA = {
    "basic_evaluation": {
        "weight_per_hour": [0.8, 1, 1, 1, 1, 0.5, 0.5, -1],
    },
    "importance": {
        "basic_evaluation": 1,
        "blank_lessons_evaluation": 1,
        "hours_per_day_evaluation": 1,
        "max_subject_hours_per_day_evaluation": 1,
        "subject_block_evaluation": 1,
        "teacher_block_evaluation": 1,
        "subject_at_end_or_start_evaluation": 1
    }
}
DEFAULT_CROSS_PARAMS = {
    "crossover_rate": 0.8,
    "mutation_rate": 0.1
}


class Day(Enum):
    MON = 0 * H_PER_DAY
    TUE = 1 * H_PER_DAY
    WED = 2 * H_PER_DAY
    THU = 3 * H_PER_DAY
    FRI = 4 * H_PER_DAY


class Config:
    def __init__(self,
                 teachers: list,
                 subjects: dict,
                 elitism: bool = True,
                 population_size: int = 100,
                 eval_criteria: dict = DEFAULT_EVAL_CRITERIA,
                 cross_params: dict = DEFAULT_CROSS_PARAMS):
        self.teachers: list = teachers
        self.subjects: dict = subjects
        self.elitism: bool = elitism
        self.population_size: int = population_size
        self.eval_criteria = eval_criteria
        self.cross_params = cross_params

    def hours_by_id(self, name: str, subject_id: str) -> int:
        for subject in self.subjects[name]:
            if subject["id"] == subject_id:
                return subject["hours"]
        return -1
