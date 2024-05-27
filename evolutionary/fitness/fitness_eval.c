#include <stdlib.h>
#include <stddef.h>
#include <fitness_eval.h>

#define H_PER_DAY 8
#define DAYS 5
#define SLOTS (H_PER_DAY * DAYS)

enum Day {
    MON = 0 * H_PER_DAY,
    TUE = 1 * H_PER_DAY,
    WED = 2 * H_PER_DAY,
    THU = 3 * H_PER_DAY,
    FRI = 4 * H_PER_DAY
}

typedef struct {
    size_t subject_id;
    size_t teacher_id;
} lesson;

typedef struct {
    size_t classes;
    t_lesson (*plan)[DAYS * H_PER_DAY];
} SchoolPlan;

SchoolPlan *create_plan(size_t classes, lesson *plan) {
    SchoolPlan *plan = malloc(sizeof(SchoolPlan));
    plan->classes = classes;
    plan->plan = malloc(classes * sizeof(lesson[DAYS * H_PER_DAY]));
    for (size_t i = 0; i < classes; i++) {
        for (size_t j = 0; j < DAYS * H_PER_DAY; j++) {
            plan->plan[i][j] = plan[i * DAYS * H_PER_DAY + j];
        }
    }

    return plan;
}

void destroy_plan(SchoolPlan *plan) {
    free(plan->plan);
    free(plan);
}

double basic_evaluation(SchoolPlan *plan, double *weights) {
    double fitness = 0;
    for (size_t i = 0; i < plan->classes; i++) {
        for (size_t j = 0; j < DAYS; j++) {
            for (size_t k = 0; k < H_PER_DAY; k++) {
                fitness += plan->plan[i][j][k].subject_id != 0 ? weights[0] : 0;
            }
        }
    }
    return fitness;
}

double blank_lessons_evaluation(SchoolPlan *plan) {
    double fitness = 0;
    for (size_t i = 0; i < plan->classes; i++) {
        for (size_t j = 0; j < DAYS; j++) {
            for (size_t k = 0; k < H_PER_DAY; k++) {
                fitness += plan->plan[i][j][k].subject_id == 0 ? 1 : 0;
            }
        }
    }
    return fitness;
}

double evaluate_fitness(SchoolPlan *plan) {
    // ...
}

double evaluate_fitness(SchoolPlan *plan) {
    // ...
}
