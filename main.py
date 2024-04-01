import random

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
DEFAULT_EVAL_CRITERIA = {}


class Config:
    def __init__(self, head_teachers, teachers, subjects):
        self.head_teachers = head_teachers
        self.teachers = teachers
        self.subjects = subjects

    def hours_by_id(self, name: str, subject_id: str) -> int:
        for subject in self.subjects[name]:
            if subject["id"] == subject_id:
                return subject["hours"]
        return -1


class SchoolPlan:  # TODO: replace again?
    def __init__(self, classes_name):
        self.fitness = -1

        plan = {"Monday": [None] * 8, "Tuesday": [None] * 8, "Wednesday": [None] * 8, "Thursday": [None] * 8,
                "Friday": [None] * 8}
        self.class_plans = {class_name: plan.copy() for class_name in classes_name}

    def generate(self, config: Config):
        def generate_plan(name):
            plan = {"Monday": [None] * 8, "Tuesday": [None] * 8, "Wednesday": [None] * 8, "Thursday": [None] * 8,
                    "Friday": [None] * 8}
            for subject in config.subjects[name]:
                hours_added = 0
                while hours_added < subject["hours"]:
                    day = random.choice(list(WEEK_DAYS))
                    hour = random.choice(range(8))
                    if plan[day][hour] is None and self.teacher_free_at(subject["teacher_id"], day, hour):
                        plan[day][hour] = {"id": subject["id"], "teacher_id": subject["teacher_id"]}
                        hours_added += 1
            return plan

        self.class_plans = {class_name: generate_plan(class_name) for class_name in config.subjects.keys()}

    def teacher_free_at(self, teacher_id: str, day: str, hour: int) -> bool:
        for name in self.class_plans.keys():
            if self.class_plans[name][day][hour] is not None and self.class_plans[name][day][hour]["teacher_id"] == teacher_id:
                return False
        return True

    def count_subject_hours(self, name: str, subject_id: str) -> int:
        hours = 0
        for day in WEEK_DAYS:
            for hour in range(8):
                if self.class_plans[name][day][hour] is not None and self.class_plans[name][day][hour]["id"] == subject_id:
                    hours += 1
        return hours

    def evaluate(self):  # TODO: send evaluation criteria from super class
        score = 0

        hours_count = [0] * 8
        for name in self.class_plans.keys():
            for day in WEEK_DAYS:
                for hour in range(8):
                    if self.class_plans[name][day][hour] is not None:
                        hours_count[hour] += 1
        score += sum(hours_count[1:6]) - hours_count[7] * 0.5 - hours_count[7] * 1

        # empty lessons FIXME: add multi hour empty lessons
        empty_lessons = 0
        for name in self.class_plans.keys():
            for day in WEEK_DAYS:
                for hour in range(1, 6):
                    if self.class_plans[name][day][hour] is None and self.class_plans[name][day][hour - 1] is not None \
                            and self.class_plans[name][day][hour + 1] is not None:
                        empty_lessons += 1
        score -= empty_lessons * 0.5

        self.fitness = score

    def swap(self, swaps=1):
        pass

    def add_to_plan(self, config: Config, name: str, day: str, hour: int, subject: dict | None) -> bool:
        if subject is None:
            self.class_plans[name][day][hour] = None
            return True

        sub_config_hours = config.hours_by_id(name, subject["id"])
        sub_current_hours = self.count_subject_hours(name, subject["id"])
        if self.class_plans[name][day][hour] is None and self.teacher_free_at(subject["teacher_id"], day, hour) \
                and sub_config_hours > sub_current_hours:
            self.class_plans[name][day][hour] = subject
            return True
        return False

    def fill_plan(self, config: Config):
        for name in self.class_plans.keys():
            for subject in config.subjects[name]:
                hours_needed = config.hours_by_id(name, subject["id"])
                while hours_needed > self.count_subject_hours(name, subject["id"]):
                    day = random.choice(WEEK_DAYS)
                    hour = random.choice(range(8))
                    if self.class_plans[name][day][hour] is None and self.teacher_free_at(subject["teacher_id"], day, hour):
                        self.class_plans[name][day][hour] = \
                            {"id": subject["id"], "teacher_id": subject["teacher_id"]}


def cross_plans(plan1: SchoolPlan, plan2: SchoolPlan, config: Config) -> SchoolPlan | None:
    DIV_FACTOR = 0.5

    child = SchoolPlan(config.head_teachers.keys())
    verification_not_needed = True
    for name in plan1.class_plans.keys():
        for day in WEEK_DAYS:
            for hour in range(8):
                lesson = plan2.class_plans[name][day][hour] if random.random() < DIV_FACTOR \
                    else plan1.class_plans[name][day][hour]
                verification_not_needed &= child.add_to_plan(config, name, day, hour, lesson)
    if verification_not_needed:
        return child
    child.fill_plan(config)
    return child


class Generation:
    def __init__(self, config: Config, size=10, crossover_rate=0.7, mutation_rate=0.1, eval_criteria=None):
        self.CROSSOVER_RATE = crossover_rate
        self.MUTATION_RATE = mutation_rate
        self.EVAL_CRITERIA = eval_criteria  # TODO: set defaults and provide option

        self.gen_no = 0
        self.size = size
        self.config = config
        self.population = [SchoolPlan(config.head_teachers.keys())] * size
        for plan in self.population:
            plan.generate(config)

    def evaluate(self):
        for plan in self.population:
            plan.evaluate()
        self.population.sort(key=lambda x: x.fitness)

    def best_plan(self) -> SchoolPlan:
        return max(self.population, key=lambda x: x.fitness)

    def statistics(self) -> dict:
        return {
            "max": self.best_plan().fitness,
            "avg": sum([plan.fitness for plan in self.population]) / self.size,
            "min": self.population[0].fitness
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
    generation = Generation(config)
    return generation
