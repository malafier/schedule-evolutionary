import random
from enum import Enum

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
H_PER_DAY = 8
DEFAULT_EVAL_CRITERIA = {}


class Day(Enum):
    MON = 0 * H_PER_DAY
    TUE = 1 * H_PER_DAY
    WED = 2 * H_PER_DAY
    THU = 3 * H_PER_DAY
    FRI = 4 * H_PER_DAY


class Config:
    def __init__(self, head_teachers, teachers, subjects):
        self.head_teachers: dict = head_teachers
        self.teachers: list = teachers
        self.subjects: dict = subjects

    def hours_by_id(self, name: str, subject_id: str) -> int:
        for subject in self.subjects[name]:
            if subject["id"] == subject_id:
                return subject["hours"]
        return -1


class SchoolPlan:  # TODO: replace again?
    def __init__(self, classes_name):
        self.fitness = -1
        self.plans = {class_name: [(0, 0) for _ in range((H_PER_DAY * len(Day)))] for class_name in classes_name}

    def generate(self, config: Config):
        def generate_group_plan(group_name: str):
            for subject in config.subjects[group_name]:
                hours_added = 0
                while hours_added < subject["hours"]:
                    day = random.choice(list(Day))
                    hour = random.choice(range(H_PER_DAY))
                    if self.plans[group_name][day.value + hour] == (0, 0) and self.teacher_free_at(subject["teacher_id"], day, hour):
                        self.plans[group_name][day.value + hour] = (subject["id"], subject["teacher_id"])
                        hours_added += 1

        for class_name in config.subjects.keys():
            generate_group_plan(class_name)

    def teacher_free_at(self, teacher_id: int, day: Day, hour: int) -> bool:
        for name in self.plans.keys():
            if self.plans[name][day.value + hour][1] == teacher_id:
                return False
        return True

    def count_subject_hours(self, group_name: str, subject_id: str) -> int:
        hours = 0
        for i in range(len(self.plans[group_name])):
            if self.plans[group_name][i][0] == subject_id:
                hours += 1
        return hours

    def evaluate(self):  # TODO: send evaluation criteria from Generation class
        score = 0

        hours_count = [0] * H_PER_DAY
        for name in self.plans.keys():
            for i in range(len(self.plans[name])):
                if self.plans[name][i] != (0, 0):
                    hours_count[i % H_PER_DAY] += 1
        score += sum(hours_count[:5]) + hours_count[6] * 0.5 - hours_count[7] * 1

        # empty lessons
        empty_lessons = [0] * H_PER_DAY
        for name in self.plans.keys():
            for day in Day:
                blank_hours = [0] * 8
                if self.plans[name][day.value] == (0, 0):
                    blank_hours[0] = 1

                for hour in range(1, H_PER_DAY):
                    if self.plans[name][day.value + hour] == (0, 0):
                        blank_hours[hour] = blank_hours[hour - 1] + 1
                    else:
                        blank_hours[hour] = 0

                for i in range(1, 7):
                    if blank_hours[i] != 0 and blank_hours[i + 1] == 0 and i != blank_hours[i]:
                        empty_lessons[blank_hours[i]] += 1
        score -= sum([empty_lessons[i] * i for i in range(6)])

        self.fitness = score

    def swap(self, swaps=1):
        pass

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
                    if self.plans[name][day.value + hour] == (0, 0) and self.teacher_free_at(subject["teacher_id"], day, hour):
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


def cross_plans(plan1: SchoolPlan, plan2: SchoolPlan, config: Config) -> SchoolPlan | None:
    if plan1.plans.keys() != plan2.plans.keys() or plan1.plans.keys() != config.head_teachers.keys():
        return None
    if plan1.plans == plan2.plans:
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
            print(f"Generated plan: {plan}")
            self.population.append(plan)

    def evaluate(self):
        for plan in self.population:
            plan.evaluate()
            print(f"Evaluated plan; fitness: {plan.fitness}")
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

    def crossover(self):
        # selection
        self.population.sort(key=lambda x: x.fitness)
        best_plan = self.best_plan()
        parents = self.population[: self.size // 2]

        # crossover
        children = []
        while len(children) < self.size - 1:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            if random.random() < self.CROSSOVER_RATE:
                child = cross_plans(parent1, parent2, self.config)
                if child is not None:
                    children.append(child)
        children.append(best_plan)
        self.population = children
        self.gen_no += 1

    def mutate(self):
        for plan in self.population:
            if random.random() < self.MUTATION_RATE:
                plan.swap()


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
                    "teacher_id": 1
                },
                {
                    "id": 2,
                    "name": "J. Angielski",
                    "hours": 3,
                    "teacher_id": 2
                },
                {
                    "id": 3,
                    "name": "Fizyka",
                    "hours": 2,
                    "teacher_id": 3
                },
                {
                    "id": 4,
                    "name": "J. Polski",
                    "hours": 4,
                    "teacher_id": 4
                },
                {
                    "id": 5,
                    "name": "Biologia",
                    "hours": 2,
                    "teacher_id": 1
                },
                {
                    "id": 6,
                    "name": "Chemia",
                    "hours": 2,
                    "teacher_id": 2
                },
                {
                    "id": 7,
                    "name": "Historia",
                    "hours": 2,
                    "teacher_id": 3
                },
                {
                    "id": 8,
                    "name": "WOS",
                    "hours": 1,
                    "teacher_id": 4
                },
                {
                    "id": 9,
                    "name": "WF",
                    "hours": 2,
                    "teacher_id": 1
                },
                {
                    "id": 10,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 2
                },
                {
                    "id": 11,
                    "name": "Godzina wychowawcza",
                    "hours": 1,
                    "teacher_id": 3
                },
                {
                    "id": 12,
                    "name": "Informatyka",
                    "hours": 2,
                    "teacher_id": 4
                }
            ],
            "1B": [
                {
                    "id": 1,
                    "name": "Matematyka",
                    "hours": 4,
                    "teacher_id": 1
                },
                {
                    "id": 2,
                    "name": "J. Angielski",
                    "hours": 3,
                    "teacher_id": 2
                },
                {
                    "id": 3,
                    "name": "Fizyka",
                    "hours": 2,
                    "teacher_id": 3
                },
                {
                    "id": 4,
                    "name": "J. Polski",
                    "hours": 4,
                    "teacher_id": 4
                },
                {
                    "id": 5,
                    "name": "Biologia",
                    "hours": 2,
                    "teacher_id": 1
                },
                {
                    "id": 6,
                    "name": "Chemia",
                    "hours": 2,
                    "teacher_id": 2
                },
                {
                    "id": 7,
                    "name": "Historia",
                    "hours": 2,
                    "teacher_id": 3
                },
                {
                    "id": 8,
                    "name": "WOS",
                    "hours": 1,
                    "teacher_id": 4
                },
                {
                    "id": 9,
                    "name": "WF",
                    "hours": 2,
                    "teacher_id": 1
                },
                {
                    "id": 10,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 2
                },
                {
                    "id": 11,
                    "name": "Godzina wychowawcza",
                    "hours": 1,
                    "teacher_id": 3
                },
                {
                    "id": 12,
                    "name": "Informatyka",
                    "hours": 2,
                    "teacher_id": 4
                }
            ]
        }
    )
    generation = Generation(config, size=100)
    return generation
