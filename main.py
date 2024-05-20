import random
from abc import ABC
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


class Day(Enum):
    MON = 0 * H_PER_DAY
    TUE = 1 * H_PER_DAY
    WED = 2 * H_PER_DAY
    THU = 3 * H_PER_DAY
    FRI = 4 * H_PER_DAY


class Config:
    def __init__(self, head_teachers: dict, teachers: list, subjects: dict):
        self.head_teachers: dict = head_teachers
        self.teachers: list = teachers
        self.subjects: dict = subjects
        self.eval_criteria = DEFAULT_EVAL_CRITERIA

    def hours_by_id(self, name: str, subject_id: str) -> int:
        for subject in self.subjects[name]:
            if subject["id"] == subject_id:
                return subject["hours"]
        return -1


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


class CrossoverStrategy(ABC):
    def crossover(self, parents, best_plan, size, crossover_rate, config: Config):
        pass

    def cross(self, plan1, plan2, config):
        pass

    def valid_plans(self, plan1: SchoolPlan, plan2: SchoolPlan, config: Config) -> bool:
        return plan1.plans.keys() == plan2.plans.keys() and plan1.plans.keys() == config.head_teachers.keys() \
            and plan1.plans != plan2.plans


# TODO: zmienić na koło rulety
class SinglePointCrossover(CrossoverStrategy):
    def crossover(self, parents, best_plan, size, crossover_rate, config: Config):
        children = []
        while len(children) < size - 1:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            if random.random() < crossover_rate:
                child = self.cross(parent1, parent2, config)
                if child is not None:
                    children.append(child)
        children.append(best_plan)
        return children

    def cross(self, plan1, plan2, config):
        if not self.valid_plans(plan1, plan2, config):
            return None

        DIV_FACTOR = 0.5

        groups = config.head_teachers.keys()
        child = SchoolPlan(groups)
        for name in groups:
            for day in list(Day):
                for hour in range(H_PER_DAY):
                    lesson = plan2.plans[name][day.value + hour] if random.random() < DIV_FACTOR \
                        else plan1.plans[name][day.value + hour]
                    child.add_to_plan(config, name, day, hour, lesson)
        child.fill_plan(config)
        return child


# TODO: jw.
class DayCrossover(CrossoverStrategy):
    def crossover(self, parents, best_plan, size, crossover_rate, config: Config):
        children = []
        while len(children) < size - 1:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            if random.random() < crossover_rate:
                child = self.cross(parent1, parent2, config)
                if child is not None:
                    children.append(child)
        children.append(best_plan)
        return children

    def cross(self, plan1, plan2, config):
        if not self.valid_plans(plan1, plan2, config):
            return None

        DIV_FACTOR = 0.5

        groups = config.head_teachers.keys()
        child = SchoolPlan(groups)
        for name in groups:
            for day in list(Day):
                plan = plan2 if random.random() < DIV_FACTOR else plan1
                for hour in range(H_PER_DAY):
                    lesson = plan.plans[name][day.value + hour]
                    child.add_to_plan(config, name, day, hour, lesson)
        child.fill_plan(config)
        return child


class ChampionCrossover(CrossoverStrategy):
    def crossover(self, parents, best_plan, size, crossover_rate, config: Config):
        children = []
        while len(children) < size - 1:
            parent2 = random.choice(parents)
            if random.random() < crossover_rate:
                child = self.cross(best_plan, parent2, config)
                if child is not None:
                    children.append(child)
        children.append(best_plan)
        return children

    def cross(self, plan1, plan2, config):
        if not self.valid_plans(plan1, plan2, config):
            return None

        groups = config.head_teachers.keys()
        child = SchoolPlan(groups)
        for name in groups:
            for day in list(Day):
                for hour in range(H_PER_DAY):
                    lesson = plan1.plans[name][day.value + hour] if plan1.fitness > plan2.fitness \
                        else plan2.plans[name][day.value + hour]
                    child.add_to_plan(config, name, day, hour, lesson)
        child.fill_plan(config)
        return child


class Generation:
    def __init__(self, config: Config, size=20, crossover_rate=0.7, mutation_rate=0.1, eval_criteria=None):
        self.CROSSOVER_RATE = crossover_rate
        self.MUTATION_RATE = mutation_rate
        self.EVAL_CRITERIA = eval_criteria  # TODO: set defaults and provide option

        self.gen_no = 0
        self.size = size
        self.config = config
        self.population = []
        for _ in range(size):
            plan = SchoolPlan(config.head_teachers.keys())
            plan.generate(config)
            # print(f"Generated plan: {plan}")
            self.population.append(plan)

    def evaluate(self):
        for plan in self.population:
            plan.evaluate(self.config)
            # print(f"Evaluated plan; fitness: {plan.fitness}")
        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def best_plan(self) -> SchoolPlan:
        return max(self.population, key=lambda x: x.fitness)

    def all(self):
        return [plan.as_dict() for plan in self.population]

    def statistics(self) -> dict:
        return {
            "max": self.best_plan().fitness,
            "avg": sum([plan.fitness for plan in self.population]) / self.size,
            "min": self.population[-1].fitness
        }

    def crossover(self, strategy: CrossoverStrategy = SinglePointCrossover()):
        # selection
        self.population.sort(key=lambda x: x.fitness)
        best_plan = self.best_plan()
        parents = self.population[: self.size // 2]

        # crossover
        self.population = strategy.crossover(parents, best_plan, self.size, self.CROSSOVER_RATE, self.config)
        self.gen_no += 1

    def mutate(self):
        for i in range(self.size - 1):
            if random.random() < self.MUTATION_RATE:
                self.population[i].swap(4)

    def purge_worst(self, min_limit: int):
        self.population = [plan for plan in self.population if plan.fitness > min_limit]
        purges = self.size - len(self.population)
        print(f"Purged {purges} worst plans")
        for _ in range(purges):
            plan = SchoolPlan(self.config.head_teachers.keys())
            plan.generate(self.config)
            self.population.append(plan)


def get_generation() -> Generation:
    config = Config(
        head_teachers={
            "1A": {
                "id": 1,
                "name": "John Doe",
                "class": "1A"
            },
            "1B": {
                "id": 2,
                "name": "Jane Doe",
                "class": "1B"
            }
        },
        teachers=[
            {
                "id": 1,
                "name": "John Doe"
            },
            {
                "id": 2,
                "name": "Jane Doe"
            },
            {
                "id": 3,
                "name": "John Smith"
            },
            {
                "id": 4,
                "name": "Jane Smith"
            }
        ],
        subjects={
            "1A": [
                {
                    "id": 1,
                    "name": "Matematyka",
                    "hours": 4,
                    "teacher_id": 1,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "J. Angielski",
                    "hours": 3,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Fizyka",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Polski",
                    "hours": 4,
                    "teacher_id": 4,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Biologia",
                    "hours": 2,
                    "teacher_id": 1,
                    "start_end": False
                },
                {
                    "id": 6,
                    "name": "Chemia",
                    "hours": 2,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 7,
                    "name": "Historia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": False
                },
                {
                    "id": 8,
                    "name": "WOS",
                    "hours": 1,
                    "teacher_id": 4,
                    "start_end": False
                },
                {
                    "id": 9,
                    "name": "WF",
                    "hours": 2,
                    "teacher_id": 1,
                    "start_end": True
                },
                {
                    "id": 10,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 2,
                    "start_end": True
                },
                {
                    "id": 11,
                    "name": "Godzina wychowawcza",
                    "hours": 1,
                    "teacher_id": 3,
                    "start_end": False
                },
                {
                    "id": 12,
                    "name": "Informatyka",
                    "hours": 2,
                    "teacher_id": 4,
                    "start_end": False
                }
            ],
            "1B": [
                {
                    "id": 1,
                    "name": "Matematyka",
                    "hours": 4,
                    "teacher_id": 1,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "J. Angielski",
                    "hours": 3,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Fizyka",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Polski",
                    "hours": 4,
                    "teacher_id": 4,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Biologia",
                    "hours": 2,
                    "teacher_id": 1,
                    "start_end": False
                },
                {
                    "id": 6,
                    "name": "Chemia",
                    "hours": 2,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 7,
                    "name": "Historia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": False
                },
                {
                    "id": 8,
                    "name": "WOS",
                    "hours": 1,
                    "teacher_id": 4,
                    "start_end": False
                },
                {
                    "id": 9,
                    "name": "WF",
                    "hours": 2,
                    "teacher_id": 1,
                    "start_end": True
                },
                {
                    "id": 10,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 2,
                    "start_end": True
                },
                {
                    "id": 11,
                    "name": "Godzina wychowawcza",
                    "hours": 1,
                    "teacher_id": 3,
                    "start_end": False
                },
                {
                    "id": 12,
                    "name": "Informatyka",
                    "hours": 2,
                    "teacher_id": 4,
                    "start_end": False
                }
            ]
        }
    )
    generation = Generation(config, size=100)
    return generation
