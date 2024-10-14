from evolutionary.config import MetaConfig


def get_config() -> MetaConfig:
    config = MetaConfig(
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
            {
                "id": 38,
                "name": "PaPa"
            },
            {
                "id": 39,
                "name": "MiMa"
            },
            {
                "id": 40,
                "name": "BaKa"
            },
            {
                "id": 41,
                "name": "ŻeWi"
            },
            {
                "id": 42,
                "name": "LaPi"
            },
            {
                "id": 43,
                "name": "KoOl"
            },
            {
                "id": 44,
                "name": "CyJa"
            },
        ],
        subjects={
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
            "5A": [
                {
                    "id": 1,
                    "name": "J. Polski",
                    "hours": 5,
                    "teacher_id": 27,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "Historia",
                    "hours": 2,
                    "teacher_id": 38,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Technika",
                    "hours": 1,
                    "teacher_id": 23,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "Matematyka",
                    "hours": 5,
                    "teacher_id": 28,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "WF",
                    "hours": 4,
                    "teacher_id": 19,
                    "start_end": False
                },
                {
                    "id": 6,
                    "name": "Muzyka",
                    "hours": 1,
                    "teacher_id": 24,
                    "start_end": False
                },
                {
                    "id": 7,
                    "name": "Plastyka",
                    "hours": 1,
                    "teacher_id": 30,
                    "start_end": False
                },
                {
                    "id": 8,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 5,
                    "start_end": True
                },
                {
                    "id": 9,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 18,
                    "start_end": False
                },
                {
                    "id": 10,
                    "name": "J. Angielski",
                    "hours": 2,
                    "teacher_id": 20,
                    "start_end": False
                },
                {
                    "id": 11,
                    "name": "Geografia",
                    "hours": 1,
                    "teacher_id": 39,
                    "start_end": False
                },
                {
                    "id": 12,
                    "name": "Biologia",
                    "hours": 1,
                    "teacher_id": 37,
                    "start_end": False
                },
                {
                    "id": 13,
                    "name": "G. Wychowawcza",
                    "hours": 1,
                    "teacher_id": 28,
                    "start_end": False
                },
            ],
            "5B": [
                {
                    "id": 1,
                    "name": "J. Polski",
                    "hours": 5,
                    "teacher_id": 40,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "Historia",
                    "hours": 2,
                    "teacher_id": 22,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Technika",
                    "hours": 1,
                    "teacher_id": 23,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "Matematyka",
                    "hours": 5,
                    "teacher_id": 28,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "WF",
                    "hours": 4,
                    "teacher_id": 41,
                    "start_end": False
                },
                {
                    "id": 6,
                    "name": "Muzyka",
                    "hours": 1,
                    "teacher_id": 24,
                    "start_end": False
                },
                {
                    "id": 7,
                    "name": "Plastyka",
                    "hours": 1,
                    "teacher_id": 30,
                    "start_end": False
                },
                {
                    "id": 8,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 5,
                    "start_end": True
                },
                {
                    "id": 9,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 31,
                    "start_end": False
                },
                {
                    "id": 10,
                    "name": "J. Angielski",
                    "hours": 2,
                    "teacher_id": 9,
                    "start_end": False
                },
                {
                    "id": 11,
                    "name": "Geografia",
                    "hours": 1,
                    "teacher_id": 39,
                    "start_end": False
                },
                {
                    "id": 12,
                    "name": "Biologia",
                    "hours": 1,
                    "teacher_id": 37,
                    "start_end": False
                },
                {
                    "id": 13,
                    "name": "G. Wychowawcza",
                    "hours": 1,
                    "teacher_id": 22,
                    "start_end": False
                },
            ],
            "5C": [
                {
                    "id": 1,
                    "name": "J. Polski",
                    "hours": 5,
                    "teacher_id": 33,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "Historia",
                    "hours": 2,
                    "teacher_id": 38,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Technika",
                    "hours": 1,
                    "teacher_id": 23,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "Matematyka",
                    "hours": 5,
                    "teacher_id": 42,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "WF",
                    "hours": 4,
                    "teacher_id": 18,
                    "start_end": False
                },
                {
                    "id": 6,
                    "name": "Muzyka",
                    "hours": 1,
                    "teacher_id": 24,
                    "start_end": False
                },
                {
                    "id": 7,
                    "name": "Plastyka",
                    "hours": 1,
                    "teacher_id": 30,
                    "start_end": False
                },
                {
                    "id": 8,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 5,
                    "start_end": True
                },
                {
                    "id": 9,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 18,
                    "start_end": False
                },
                {
                    "id": 10,
                    "name": "J. Angielski",
                    "hours": 2,
                    "teacher_id": 43,
                    "start_end": False
                },
                {
                    "id": 11,
                    "name": "Geografia",
                    "hours": 1,
                    "teacher_id": 39,
                    "start_end": False
                },
                {
                    "id": 12,
                    "name": "Biologia",
                    "hours": 1,
                    "teacher_id": 37,
                    "start_end": False
                },
                {
                    "id": 13,
                    "name": "G. Wychowawcza",
                    "hours": 1,
                    "teacher_id": 33,
                    "start_end": False
                },
            ],
            "5D": [
                {
                    "id": 1,
                    "name": "J. Polski",
                    "hours": 5,
                    "teacher_id": 27,
                    "start_end": False
                },
                {
                    "id": 2,
                    "name": "Historia",
                    "hours": 2,
                    "teacher_id": 38,
                    "start_end": False
                },
                {
                    "id": 3,
                    "name": "Technika",
                    "hours": 1,
                    "teacher_id": 23,
                    "start_end": False
                },
                {
                    "id": 4,
                    "name": "Matematyka",
                    "hours": 5,
                    "teacher_id": 42,
                    "start_end": False
                },
                {
                    "id": 5,
                    "name": "WF",
                    "hours": 4,
                    "teacher_id": 44,
                    "start_end": False
                },
                {
                    "id": 6,
                    "name": "Muzyka",
                    "hours": 1,
                    "teacher_id": 24,
                    "start_end": False
                },
                {
                    "id": 7,
                    "name": "Plastyka",
                    "hours": 1,
                    "teacher_id": 30,
                    "start_end": False
                },
                {
                    "id": 8,
                    "name": "Religia",
                    "hours": 2,
                    "teacher_id": 5,
                    "start_end": True
                },
                {
                    "id": 9,
                    "name": "Informatyka",
                    "hours": 1,
                    "teacher_id": 18,
                    "start_end": False
                },
                {
                    "id": 10,
                    "name": "J. Angielski",
                    "hours": 2,
                    "teacher_id": 43,
                    "start_end": False
                },
                {
                    "id": 11,
                    "name": "Geografia",
                    "hours": 1,
                    "teacher_id": 39,
                    "start_end": False
                },
                {
                    "id": 12,
                    "name": "Biologia",
                    "hours": 1,
                    "teacher_id": 37,
                    "start_end": False
                },
                {
                    "id": 13,
                    "name": "G. Wychowawcza",
                    "hours": 1,
                    "teacher_id": 44,
                    "start_end": False
                },
            ],
        }
    )
    return config
