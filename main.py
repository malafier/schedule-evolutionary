from evolutionary.config import Config
from evolutionary.generation import Generation


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
