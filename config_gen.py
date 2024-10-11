from evolutionary.config import Config


def get_config() -> Config:
    config = Config(
        population_size=100,
        teachers=[
            {
                "id": 1,
                "name": "FiJu"
            },
            {
                "id": 2,
                "name": "KoWe"
            },
            {
                "id": 3,
                "name": "JaIw"
            },
            {
                "id": 4,
                "name": "TrMa"
            },
            {
                "id": 5,
                "name": "SoJo"
            },
            {
                "id": 6,
                "name": "KiAn"
            },
            {
                "id": 7,
                "name": "WoAg"
            },
            {
                "id": 8,
                "name": "GrAg"
            },
            {
                "id": 9,
                "name": "WłAl"
            },
            {
                "id": 10,
                "name": "SzBa"
            },
            {
                "id": 11,
                "name": "KaKa"
            },
            {
                "id": 12,
                "name": "MiDo"
            },
            {
                "id": 13,
                "name": "KrKa"
            },
            {
                "id": 14,
                "name": "SzŻa"
            },
            {
                "id": 15,
                "name": "LeAg"
            },
            {
                "id": 16,
                "name": "JaJo"
            },
            {
                "id": 17,
                "name": "WrEl"
            },
            {
                "id": 18,
                "name": "TK"
            },
            {
                "id": 19,
                "name": "KuPi"
            },
            {
                "id": 20,
                "name": "GrHa"
            },
            {
                "id": 21,
                "name": "HF"
            },
            {
                "id": 22,
                "name": "BoBa"
            },
            {
                "id": 23,
                "name": "MiIg"
            },
            {
                "id": 24,
                "name": "GąAg"
            },
            {
                "id": 25,
                "name": "CiKa"
            },
            {
                "id": 26,
                "name": "MaMa"
            },
            {
                "id": 27,
                "name": "NoAn"
            },
            {
                "id": 28,
                "name": "SoBe"
            },
            {
                "id": 29,
                "name": "AnBe"
            },
            {
                "id": 30,
                "name": "ByAl"
            },
            {
                "id": 31,
                "name": "KaMa"
            },
            {
                "id": 32,
                "name": "KaKa"
            },
            {
                "id": 33,
                "name": "TuEl"
            },
            {
                "id": 34,
                "name": "AF"
            },
            {
                "id": 35,
                "name": "WrJu"
            },
            {
                "id": 36,
                "name": "SoGa"
            },
            {
                "id": 37,
                "name": "GoKa"
            },
        ],
        subjects={
            "1A": [
                {
                    "id": 1,
                    "name": "Edu. Wcz.",
                    "hours": 14,
                    "teacher_id": 1,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "WF",
                    "hours": 3,
                    "teacher_id": 1,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 1,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Angielski",
                    "hours": 2,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": True
                },
            ],
            "1B": [
                {
                    "id": 1,
                    "name": "Edu. Wcz.",
                    "hours": 14,
                    "teacher_id": 4,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "WF",
                    "hours": 3,
                    "teacher_id": 4,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 4,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Angielski",
                    "hours": 2,
                    "teacher_id": 5,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": True
                },
            ],
            "1C": [
                {
                    "id": 1,
                    "name": "Edu. Wcz.",
                    "hours": 14,
                    "teacher_id": 6,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "WF",
                    "hours": 3,
                    "teacher_id": 6,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 6,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Angielski",
                    "hours": 2,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": True
                },
            ],
            "1D": [
                {
                    "id": 1,
                    "name": "Edu. Wcz.",
                    "hours": 14,
                    "teacher_id": 7,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "WF",
                    "hours": 3,
                    "teacher_id": 7,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 7,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Angielski",
                    "hours": 2,
                    "teacher_id": 7,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": True
                },
            ],
            "2A": [
                {
                    "id": 1,
                    "name": "Edu. Wcz.",
                    "hours": 14,
                    "teacher_id": 8,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "WF",
                    "hours": 3,
                    "teacher_id": 8,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 8,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Angielski",
                    "hours": 3,
                    "teacher_id": 9,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": True
                },
            ],
            "2B": [
                {
                    "id": 1,
                    "name": "Edu. Wcz.",
                    "hours": 14,
                    "teacher_id": 10,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "WF",
                    "hours": 3,
                    "teacher_id": 10,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 10,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Angielski",
                    "hours": 3,
                    "teacher_id": 11,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": True
                },
            ],
            "2C": [
                {
                    "id": 1,
                    "name": "Edu. Wcz.",
                    "hours": 14,
                    "teacher_id": 12,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "WF",
                    "hours": 3,
                    "teacher_id": 12,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 12,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Angielski",
                    "hours": 3,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": True
                },
            ],
            "2D": [
                {
                    "id": 1,
                    "name": "Edu. Wcz.",
                    "hours": 14,
                    "teacher_id": 13,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "WF",
                    "hours": 3,
                    "teacher_id": 13,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 13,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Angielski",
                    "hours": 3,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": False
                },
            ],
            "3A" :[
                {
                    "id": 1,
                    "name": "Edu. Wcz.",
                    "hours": 14,
                    "teacher_id": 14,
                    "start_end": False
                },
                {
                    "id": 1,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 14,
                    "start_end": False
                },
                {
                    "id": 1,
                    "name": "WF",
                    "hours": 3,
                    "teacher_id": 14,
                    "start_end": False
                },
                {
                    "id": 1,
                    "name": "J. Angielski",
                    "hours": 3,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 5,
                    "start_end": False
                },
            ],
            "3B": [
                {
                    "id": 1,
                    "name": "Edu. Wcz.",
                    "hours": 14,
                    "teacher_id": 14,
                    "start_end": False
                },
                {
                    "id": 1,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 14,
                    "start_end": False
                },
                {
                    "id": 1,
                    "name": "WF",
                    "hours": 3,
                    "teacher_id": 14,
                    "start_end": False
                },
                {
                    "id": 1,
                    "name": "J. Angielski",
                    "hours": 3,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 5,
                    "start_end": False
                },
            ],
            "3C": [
                {
                    "id": 1,
                    "name": "Edu. Wcz.",
                    "hours": 14,
                    "teacher_id": 15,
                    "start_end": False
                },
                {
                    "id": 1,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 15,
                    "start_end": False
                },
                {
                    "id": 1,
                    "name": "WF",
                    "hours": 3,
                    "teacher_id": 15,
                    "start_end": False
                },
                {
                    "id": 1,
                    "name": "J. Angielski",
                    "hours": 3,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 5,
                    "start_end": False
                },
            ],
            "3D": [
                {
                    "id": 1,
                    "name": "Edu. Wcz.",
                    "hours": 14,
                    "teacher_id": 16,
                    "start_end": False
                },
                {
                    "id": 1,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 16,
                    "start_end": False
                },
                {
                    "id": 1,
                    "name": "WF",
                    "hours": 3,
                    "teacher_id": 16,
                    "start_end": False
                },
                {
                    "id": 1,
                    "name": "J. Angielski",
                    "hours": 3,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 5,
                    "start_end": False
                },
            ],
            "4A": [
                {
                    "id": 1,
                    "name": "J. Polski",
                    "hours": 5,
                    "teacher_id": 17,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 18,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "WF",
                    "hours": 4,
                    "teacher_id": 19,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Angielski",
                    "hours": 2,
                    "teacher_id": 20,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Matematyka",
                    "hours": 4,
                    "teacher_id": 21,
                    "start_end": False
                },
                {
                    "id": 6,
                    "name": "Historia",
                    "hours": 1,
                    "teacher_id": 22,
                    "start_end": False
                },
                {
                    "id": 7,
                    "name": "Technika",
                    "hours": 1,
                    "teacher_id": 23,
                    "start_end": False
                },
                {
                    "id": 8,
                    "name": "Muzyka",
                    "hours": 1,
                    "teacher_id": 24,
                    "start_end": False
                },
                {
                    "id": 9,
                    "name": "Plastyka",
                    "hours": 1,
                    "teacher_id": 25,
                    "start_end": False
                },
                {
                    "id": 10,
                    "name": "Przyroda",
                    "hours": 2,
                    "teacher_id": 26,
                    "start_end": False
                },
                {
                    "id": 11,
                    "name": "G. Wychowawcza",
                    "hours": 1,
                    "teacher_id": 19,
                    "start_end": False
                },
                {
                    "id": 12,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": True
                },
            ],
            "4B": [
                {
                    "id": 1,
                    "name": "J. Polski",
                    "hours": 5,
                    "teacher_id": 27,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 31,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "WF",
                    "hours": 4,
                    "teacher_id": 29,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Angielski",
                    "hours": 2,
                    "teacher_id": 32,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Matematyka",
                    "hours": 4,
                    "teacher_id": 28,
                    "start_end": False
                },
                {
                    "id": 6,
                    "name": "Historia",
                    "hours": 1,
                    "teacher_id": 22,
                    "start_end": False
                },
                {
                    "id": 7,
                    "name": "Technika",
                    "hours": 1,
                    "teacher_id": 23,
                    "start_end": False
                },
                {
                    "id": 8,
                    "name": "Muzyka",
                    "hours": 1,
                    "teacher_id": 24,
                    "start_end": False
                },
                {
                    "id": 9,
                    "name": "Plastyka",
                    "hours": 1,
                    "teacher_id": 30,
                    "start_end": False
                },
                {
                    "id": 10,
                    "name": "Przyroda",
                    "hours": 2,
                    "teacher_id": 26,
                    "start_end": False
                },
                {
                    "id": 11,
                    "name": "G. Wychowawcza",
                    "hours": 1,
                    "teacher_id": 32,
                    "start_end": False
                },
                {
                    "id": 12,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": True
                },
            ],
            "4C": [
                {
                    "id": 1,
                    "name": "J. Polski",
                    "hours": 5,
                    "teacher_id": 33,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "WF",
                    "hours": 4,
                    "teacher_id": 18,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Angielski",
                    "hours": 2,
                    "teacher_id": 36,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Matematyka",
                    "hours": 4,
                    "teacher_id": 35,
                    "start_end": False
                },
                {
                    "id": 6,
                    "name": "Historia",
                    "hours": 1,
                    "teacher_id": 22,
                    "start_end": False
                },
                {
                    "id": 7,
                    "name": "Technika",
                    "hours": 1,
                    "teacher_id": 23,
                    "start_end": False
                },
                {
                    "id": 8,
                    "name": "Muzyka",
                    "hours": 1,
                    "teacher_id": 24,
                    "start_end": False
                },
                {
                    "id": 9,
                    "name": "Plastyka",
                    "hours": 1,
                    "teacher_id": 30,
                    "start_end": False
                },
                {
                    "id": 10,
                    "name": "Przyroda",
                    "hours": 2,
                    "teacher_id": 26,
                    "start_end": False
                },
                {
                    "id": 11,
                    "name": "G. Wychowawcza",
                    "hours": 1,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 12,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": True
                },
            ],
            "4D": [
                {
                    "id": 1,
                    "name": "J. Polski",
                    "hours": 5,
                    "teacher_id": 33,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 2,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "WF",
                    "hours": 4,
                    "teacher_id": 29,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "J. Angielski",
                    "hours": 2,
                    "teacher_id": 32,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "Matematyka",
                    "hours": 4,
                    "teacher_id": 34,
                    "start_end": False
                },
                {
                    "id": 6,
                    "name": "Historia",
                    "hours": 1,
                    "teacher_id": 22,
                    "start_end": False
                },
                {
                    "id": 7,
                    "name": "Technika",
                    "hours": 1,
                    "teacher_id": 23,
                    "start_end": False
                },
                {
                    "id": 8,
                    "name": "Muzyka",
                    "hours": 1,
                    "teacher_id": 24,
                    "start_end": False
                },
                {
                    "id": 9,
                    "name": "Plastyka",
                    "hours": 1,
                    "teacher_id": 30,
                    "start_end": False
                },
                {
                    "id": 10,
                    "name": "Przyroda",
                    "hours": 2,
                    "teacher_id": 26,
                    "start_end": False
                },
                {
                    "id": 11,
                    "name": "G. Wychowawcza",
                    "hours": 1,
                    "teacher_id": 37,
                    "start_end": False
                },
                {
                    "id": 12,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 3,
                    "start_end": True
                },
            ],
        }
    )
    return config
