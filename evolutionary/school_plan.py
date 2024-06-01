import random

from evolutionary.config import WEEK_DAYS, H_PER_DAY, Day, Config
from evolutionary.evaluation import basic_evaluation, blank_lessons_evaluation, hours_per_day_evaluation, \
    max_subject_hours_per_day_evaluation, subject_block_evaluation, teacher_block_evaluation, \
    subject_at_end_or_start_evaluation


class SchoolPlan:
    def __init__(self, classes_name, plans=None):
        self.fitness: float = 0
        self.plans: dict = {class_name: [(0, 0) for _ in range((H_PER_DAY * len(Day)))] for class_name in classes_name} \
            if plans is None else plans

    def generate(self, config: Config):
        def generate_group_plan(group_name: str):
            for subject in config.subjects[group_name]:
                hours_added = 0
                while hours_added < subject["hours"]:
                    day = random.choice(list(Day))
                    hour = random.choice(range(H_PER_DAY))
                    if self.plans[group_name][day.value + hour] == (0, 0) and self.teacher_free_at(
                            subject["teacher_id"], day, hour):
                        self.plans[group_name][day.value + hour] = (subject["id"], subject["teacher_id"])
                        hours_added += 1

        for class_name in config.subjects.keys():
            generate_group_plan(class_name)

    def teacher_free_at(self, teacher_id: int, day, hour: int) -> bool:
        if isinstance(day, Day):
            day = day.value
        for name in self.plans.keys():
            if self.plans[name][day + hour][1] == teacher_id:
                return False
        return True

    def count_subject_hours(self, group_name: str, subject_id: str) -> int:
        hours = 0
        for i in range(len(self.plans[group_name])):
            if self.plans[group_name][i][0] == subject_id:
                hours += 1
        return hours

    def evaluate(self, config: Config):
        importance = config.eval_criteria["importance"]

        score = 0
        score += (importance["basic_evaluation"] *
                  basic_evaluation(self.plans, config.eval_criteria["basic_evaluation"]["weight_per_hour"]))
        score += (importance["blank_lessons_evaluation"] *  # TODO: *= instead of += -- that change might alter behaviour of the algorithm
                  blank_lessons_evaluation(self.plans))
        score += (importance["hours_per_day_evaluation"] *
                  hours_per_day_evaluation(self.plans))
        score += (importance["max_subject_hours_per_day_evaluation"] *
                  max_subject_hours_per_day_evaluation(self.plans, config.subjects))
        score += (importance["subject_block_evaluation"] *
                  subject_block_evaluation(self.plans, 0, -5, config.subjects))
        score += (importance["teacher_block_evaluation"] *
                  teacher_block_evaluation(self.plans, 1, -2, config.teachers))
        score += (importance["subject_at_end_or_start_evaluation"] *
                  subject_at_end_or_start_evaluation(self.plans, config.subjects))

        self.fitness = score

    def swap(self, swaps=1):
        for i in range(swaps):
            lesson1 = random.choice(list(Day)).value + random.choice(range(H_PER_DAY))
            lesson2 = random.choice(list(Day)).value + random.choice(range(H_PER_DAY))
            group = random.choice(list(self.plans.keys()))

            teachers_ok = True
            if self.plans[group][lesson1] != (0, 0):
                teacher1 = self.plans[group][lesson1][1]
                teachers_ok &= self.teacher_free_at(teacher1, lesson2 // H_PER_DAY, lesson2 % H_PER_DAY) or \
                               self.plans[group][lesson2][1] == teacher1
            if self.plans[group][lesson2] != (0, 0):
                teacher2 = self.plans[group][lesson2][1]
                teachers_ok &= self.teacher_free_at(teacher2, lesson1 // H_PER_DAY, lesson1 % H_PER_DAY) or \
                               self.plans[group][lesson1][1] == teacher2
            if teachers_ok:
                self.plans[group][lesson1], self.plans[group][lesson2] = self.plans[group][lesson2], self.plans[group][
                    lesson1]
            else:
                i -= 1

    def add_to_plan(self, config: Config, name: str, day: Day, hour: int, subject: tuple):
        if subject == (0, 0):
            self.plans[name][day.value + hour] = (0, 0)
            return

        sub_config_hours = config.hours_by_id(name, subject[0])
        sub_current_hours = self.count_subject_hours(name, subject[0])
        if self.plans[name][day.value + hour] == (0, 0) and self.teacher_free_at(subject[1], day, hour) \
                and sub_config_hours > sub_current_hours:
            self.plans[name][day.value + hour] = (subject[0], subject[1])

    def fill_plan(self, config: Config):
        for name in self.plans.keys():
            for subject in config.subjects[name]:
                hours_needed = config.hours_by_id(name, subject["id"])
                while hours_needed > self.count_subject_hours(name, subject["id"]):
                    day = random.choice(list(Day))
                    hour = random.choice(range(H_PER_DAY))
                    if (self.plans[name][day.value + hour] == (0, 0) and
                            self.teacher_free_at(subject["teacher_id"], day, hour)):
                        self.plans[name][day.value + hour] = (subject["id"], subject["teacher_id"])

    def as_dict(self) -> dict:
        school_plan = {name: {day: [] for day in WEEK_DAYS} for name in self.plans.keys()}
        for name in self.plans.keys():
            for day in list(Day):
                for hour in range(H_PER_DAY):
                    subject_id, teacher_id = self.plans[name][day.value + hour]
                    week_day = WEEK_DAYS[day.value // H_PER_DAY]
                    school_plan[name][week_day].append({
                        "subject_id": subject_id,
                        "teacher_id": teacher_id
                    })
        return school_plan

    def __str__(self):
        return str(self.plans)
