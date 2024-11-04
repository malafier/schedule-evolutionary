import random

from evolutionary.config import WEEK_DAYS, H_PER_DAY, Day, Config, MetaConfig
from evolutionary.evaluation import basic_evaluation, gaps_evaluation, hours_per_day_evaluation, \
    max_subject_hours_per_day_evaluation, subject_block_evaluation, teacher_block_evaluation, \
    subject_at_end_or_start_evaluation


class SchoolPlan:
    def __init__(self, no_groups, plans=None):
        self.fitness: float = 0
        self.plans: list = [[(0, 0) for _ in range((H_PER_DAY * len(Day)))] for _ in range(no_groups)] \
            if plans is None else plans

    def generate(self, config: Config):
        def generate_group_plan(gid: int):
            for subject in config.subjects[gid]:
                hours_added = 0
                while hours_added < subject["hours"]:
                    day = random.choice(list(Day))
                    hour = random.choice(range(H_PER_DAY))
                    if self.plans[gid][day.value + hour] == (0, 0) and self.teacher_free_at(
                            subject["teacher_id"], day, hour):
                        self.plans[gid][day.value + hour] = (subject["id"], subject["teacher_id"])
                        hours_added += 1

        for idx in range(config.no_groups):
            generate_group_plan(idx)

    def teacher_free_at(self, teacher_id: int, day: int, hour: int) -> bool:
        if isinstance(day, Day):
            day = day.value
        for plan in self.plans:
            if plan[day + hour][1] == teacher_id:
                return False
        return True

    def count_subject_hours(self, gid: int, subject_id: int) -> int:
        hours = 0
        for i in range(len(self.plans[gid])):
            if self.plans[gid][i][0] == subject_id:
                hours += 1
        return hours

    def evaluate(self, config: Config):
        score = config.eval.basic_imp * basic_evaluation(self.plans, config.eval.hours_weight)\
            + config.eval.hpd_imp * hours_per_day_evaluation(self.plans)\
            + config.eval.max_subj_hpd_imp * max_subject_hours_per_day_evaluation(self.plans, config.subjects)\
            + config.eval.subj_block_imp * subject_block_evaluation(self.plans, 0, -5, config.subjects)\
            + config.eval.teach_block_imp * teacher_block_evaluation(self.plans, 1, -2, config.teachers)\
            + config.eval.subj_end_start_imp * subject_at_end_or_start_evaluation(self.plans, config.subjects)

        score *= config.eval.gap_imp * gaps_evaluation(self.plans)

        self.fitness = score

    def swap(self, swaps=1):
        for i in range(swaps):
            lesson1 = random.choice(list(Day)).value + random.choice(range(H_PER_DAY))
            lesson2 = random.choice(list(Day)).value + random.choice(range(H_PER_DAY))
            gid = random.choice(range(len(self.plans)))

            teachers_ok = True
            if self.plans[gid][lesson1] != (0, 0):
                teacher1 = self.plans[gid][lesson1][1]
                teachers_ok &= self.teacher_free_at(teacher1, lesson2 // H_PER_DAY, lesson2 % H_PER_DAY) or \
                               self.plans[gid][lesson2][1] == teacher1
            if self.plans[gid][lesson2] != (0, 0):
                teacher2 = self.plans[gid][lesson2][1]
                teachers_ok &= self.teacher_free_at(teacher2, lesson1 // H_PER_DAY, lesson1 % H_PER_DAY) or \
                               self.plans[gid][lesson1][1] == teacher2

            if teachers_ok:
                self.plans[gid][lesson1], self.plans[gid][lesson2] = self.plans[gid][lesson2], self.plans[gid][lesson1]
            else:
                i -= 1

    def add_to_plan(self, config: Config, gid: int, day: Day, hour: int, subject: tuple):
        if subject == (0, 0):
            self.plans[gid][day.value + hour] = (0, 0)
            return

        sub_config_hours = config.hours_by_id(gid, subject[0])
        sub_current_hours = self.count_subject_hours(gid, subject[0])
        if self.plans[gid][day.value + hour] == (0, 0) \
                and self.teacher_free_at(subject[1], day, hour) \
                and sub_config_hours > sub_current_hours:
            self.plans[gid][day.value + hour] = (subject[0], subject[1])

    def fill_plan(self, config: Config):
        for gid, plan in enumerate(self.plans):
            for subject in config.subjects[gid]:
                hours_needed = config.hours_by_id(gid, subject["id"])
                while hours_needed > self.count_subject_hours(gid, subject["id"]):
                    day = random.choice(list(Day))
                    hour = random.choice(range(H_PER_DAY))
                    if plan[day.value + hour] == (0, 0) and self.teacher_free_at(subject["teacher_id"], day, hour):
                        plan[day.value + hour] = (subject["id"], subject["teacher_id"])

    def as_dict(self, config: MetaConfig) -> dict:
        school_plan = {name: {day: [] for day in WEEK_DAYS} for name in config.group_to_id.values()}
        for gid in range(len(self.plans)):
            for day in list(Day):
                for hour in range(H_PER_DAY):
                    sub_id, teach_id = self.plans[gid][day.value + hour]
                    week_day = WEEK_DAYS[day.value // H_PER_DAY]
                    school_plan[config.group_to_id[gid]][week_day].append({
                        "subject_id": sub_id,
                        "teacher_id": teach_id
                    })
        return school_plan

    def __str__(self):
        return str(self.plans)
