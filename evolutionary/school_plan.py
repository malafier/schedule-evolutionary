import random

from evolutionary.config import WEEK_DAYS, H_PER_DAY, Day, Config


def basic_evaluation(plan, weight_per_hour: list):
    score = 0
    hours_count = [0] * H_PER_DAY
    for name in plan.keys():
        for i in range(len(plan[name])):
            if plan[name][i] != (0, 0):
                hours_count[i % H_PER_DAY] += 1
    for i in range(len(hours_count)):
        score += weight_per_hour[i] * hours_count[i]
    return score


def blank_lessons_evaluation(plan):
    def is_empty(group_name: str, x_day: Day, start_h: int, h_span: int) -> bool:
        lessons = plan[group_name][x_day.value + start_h: x_day.value + start_h + h_span - 1]
        lesson_before = plan[group_name][x_day.value + start_h - 1]
        lesson_after = plan[group_name][x_day.value + start_h + h_span]
        return all([lesson == (0, 0) for lesson in lessons]) and lesson_after != (0, 0) and lesson_before != (0, 0)

    score = 0
    for name in plan.keys():
        for day in Day:
            for empty_size in range(1, 7):
                for lesson_h in range(1, H_PER_DAY - empty_size):
                    if is_empty(name, day, lesson_h, empty_size):
                        score += empty_size
    return -score


def hours_per_day_evaluation(plan):
    score = 0
    for name in plan.keys():
        for day in Day:
            hours = 0
            for i in range(H_PER_DAY):
                if plan[name][day.value + i] != (0, 0):
                    hours += 1
            score += 1 if hours <= 6 else -hours
    return score


def max_subject_hours_per_day_evaluation(plan, config: Config):
    score = 0
    for name in plan.keys():
        for day in Day:
            for subject in config.subjects[name]:
                hours = 0
                for i in range(H_PER_DAY):
                    if plan[name][day.value + i][0] == subject["id"]:
                        hours += 1
                score += 1 if hours <= 2 else -hours
    return score


def subject_block_evaluation(plan, reward, punishment, config: Config):
    score = 0
    for name in plan.keys():
        for day in Day:
            for subject in config.subjects[name]:
                hours = []
                for i in range(H_PER_DAY):
                    if plan[name][day.value + i][0] == subject["id"]:
                        hours.append(i)
                if len(hours) > 1:
                    for i in range(len(hours) - 1):
                        if hours[i + 1] - hours[i] == 1:
                            score += reward
                        else:
                            score += punishment
    return score


def teacher_block_evaluation(plan, reward, punishment, config: Config):
    score = 0
    teachers = config.teachers
    for teacher in teachers:
        for day in Day:
            lessons = []
            for name in plan.keys():
                for i in range(H_PER_DAY):
                    if plan[name][day.value + i][1] == teacher["id"]:
                        lessons.append((name, i))
            if len(lessons) > 1:
                for i in range(len(lessons) - 1):
                    if lessons[i + 1][1] - lessons[i][1] == 1:
                        score += reward
                    else:
                        score += punishment
    return score


def subject_at_end_or_start_evaluation(plan, config: Config):
    score = 0
    for name in plan.keys():
        special_subjects = filter(lambda x: x["start_end"], config.subjects[name])
        for subject in special_subjects:
            for day in Day:
                for i in range(H_PER_DAY):
                    first_or_last = (
                            i == 0 or
                            i == H_PER_DAY - 1 or
                            all([plan[name][day.value: day.value + i] == (0, 0)]) or
                            all([plan[name][day.value + i + 1: day.value + H_PER_DAY] == (0, 0)])
                    )
                    if plan[name][day.value + i] == subject["id"] and first_or_last:
                        score += 1
    return score


class SchoolPlan:
    def __init__(self, classes_name):
        self.fitness = 0
        self.plans = {class_name: [(0, 0) for _ in range((H_PER_DAY * len(Day)))] for class_name in classes_name}

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
        score += importance["basic_evaluation"] * basic_evaluation(self.plans, config.eval_criteria["basic_evaluation"][
            "weight_per_hour"])
        score += importance["blank_lessons_evaluation"] * blank_lessons_evaluation(self.plans)
        score += importance["hours_per_day_evaluation"] * hours_per_day_evaluation(self.plans)
        score += importance["max_subject_hours_per_day_evaluation"] * max_subject_hours_per_day_evaluation(self.plans,
                                                                                                           config)
        score += importance["subject_block_evaluation"] * subject_block_evaluation(self.plans, 0, -5, config)
        score += importance["teacher_block_evaluation"] * teacher_block_evaluation(self.plans, 1, -2, config)
        score += importance["subject_at_end_or_start_evaluation"] * subject_at_end_or_start_evaluation(self.plans,
                                                                                                       config)

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
                    if self.plans[name][day.value + hour] == (0, 0) and self.teacher_free_at(subject["teacher_id"], day,
                                                                                             hour):
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
