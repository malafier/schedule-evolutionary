import math
import random

from evolutionary.config import WEEK_DAYS, H_PER_DAY, Day, Config, MetaConfig
from evolutionary.evaluation import basic_evaluation, gaps_evaluation, hours_per_day_evaluation, \
    max_subject_hours_per_day_evaluation, subject_block_evaluation, teacher_block_evaluation, \
    subject_at_end_or_start_evaluation
from evolutionary.fixing_algorithm import teacher_matrix, fix_late_gaps
from evolutionary.mutation import mutate

Matrix = list[list[int]]


class SchoolPlan:
    def __init__(self, no_groups, plans=None):
        self.fitness: float = 0
        self.plans: Matrix = [[0 for _ in range((H_PER_DAY * len(Day)))] for _ in range(no_groups)] \
            if plans is None else plans

    def generate(self, config: Config):
        def generate_group_plan(gid: int):
            for subject in config.subjects[gid]:
                hours_added = 0
                while hours_added < subject["hours"]:
                    day = random.choice(list(Day))
                    hour = random.choice(range(H_PER_DAY))
                    if self.plans[gid][day.value + hour] == 0 and self.teacher_free_at(
                            subject["teacher_id"], day, hour, config):
                        self.plans[gid][day.value + hour] = subject["id"]
                        hours_added += 1

        for idx in range(config.no_groups):
            generate_group_plan(idx)

    def teacher_free_at(self, teacher_id: int, day: int, hour: int, config: Config) -> bool:
        if isinstance(day, Day):
            day = day.value
        for gid, plan in enumerate(self.plans):
            if config.teacher_by_subject(gid, plan[day + hour]) == teacher_id:
                return False
        return True

    def count_subject_hours(self, gid: int, subject_id: int) -> int:
        hours = 0
        for i in range(len(self.plans[gid])):
            if self.plans[gid][i] == subject_id:
                hours += 1
        return hours

    def evaluate(self, config: Config):
        self.fitness = (
                        config.eval.basic_imp * basic_evaluation(self.plans, config.eval.hours_weight)
                        + config.eval.hpd_imp * hours_per_day_evaluation(self.plans)
                        + config.eval.max_subj_hpd_imp * max_subject_hours_per_day_evaluation(self.plans, config.subjects)
                        + config.eval.subj_block_imp * subject_block_evaluation(self.plans, config.subjects)
                        + config.eval.subj_end_start_imp * subject_at_end_or_start_evaluation(self.plans, config.subjects)
                        + config.eval.teach_block_imp * teacher_block_evaluation(
                    teacher_matrix(self.plans, config.sub_to_teach), config.teachers
                )
                ) / math.log2(1 + config.eval.gap_imp * gaps_evaluation(self.plans))

    def mutate(self, config: Config):
        self.plans = mutate(self.plans, config.sub_to_teach)

    def fix(self, config: Config):
        self.plans = fix_late_gaps(self.plans, config.sub_to_teach)

    def add_to_plan(self, config: Config, gid: int, day: Day, hour: int, subject: int):
        if subject == (0, 0):
            self.plans[gid][day.value + hour] = 0
            return

        sub_config_hours = config.hours_by_id(gid, subject)
        sub_current_hours = self.count_subject_hours(gid, subject)
        if self.plans[gid][day.value + hour] == (0, 0) \
                and self.teacher_free_at(config.teacher_by_subject(gid, subject), day, hour, config) \
                and sub_config_hours > sub_current_hours:
            self.plans[gid][day.value + hour] = subject

    def fill_plan(self, config: Config):
        for gid, plan in enumerate(self.plans):
            for subject in config.subjects[gid]:
                hours_needed = config.hours_by_id(gid, subject["id"])
                while hours_needed > self.count_subject_hours(gid, subject["id"]):
                    day = random.choice(list(Day))
                    hour = random.choice(range(H_PER_DAY))
                    if plan[day.value + hour] == 0 and self.teacher_free_at(subject["teacher_id"], day, hour, config):
                        plan[day.value + hour] = subject["id"]

    def as_dict(self, config: Config) -> dict:
        school_plan = {name: {day: [] for day in WEEK_DAYS} for name in config.group_to_id.values()}
        for gid in range(len(self.plans)):
            for day in list(Day):
                for hour in range(H_PER_DAY):
                    sub_id = self.plans[gid][day.value + hour]
                    teach_id = config.sub_to_teach[gid][sub_id] if sub_id != 0 else 0
                    week_day = WEEK_DAYS[day.value // H_PER_DAY]
                    school_plan[config.group_to_id[gid]][week_day].append({
                        "subject_id": sub_id,
                        "teacher_id": teach_id
                    })
        return school_plan

    def teachers_plans(self, config: Config):
        matrix = teacher_matrix(self.plans, config.sub_to_teach)
        max_idx = max([t["id"] for t in config.teachers])
        teachers = [{day: [] for day in WEEK_DAYS} for _ in range(max_idx+1)]

        for i in range(1, max_idx+1):
            for day in list(Day):
                for hour in range(H_PER_DAY):
                    is_teaching = False
                    for gid in range(config.no_groups):
                        if matrix[gid][day.value + hour] == i:
                            is_teaching = True
                            break

                    week_day = WEEK_DAYS[day.value // H_PER_DAY]
                    teachers[i][week_day].append(is_teaching)
        return teachers

    def __str__(self):
        return str(self.plans)
