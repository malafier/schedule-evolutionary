#ifndef FITNESS_EVAL_H
#define FITNESS_EVAL_H

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

double evaluate_fitness(int *plans, int num_classes, int num_slots);

#endif // FITNESS_EVAL_H