import cython
from libc.stdlib cimport rand

cdef int H_PER_DAY = 8

cdef class Day:
    MON = 0 * H_PER_DAY
    TUE = 1 * H_PER_DAY
    WED = 2 * H_PER_DAY
    THU = 3 * H_PER_DAY
    FRI = 4 * H_PER_DAY

    cdef list _days

    def __cinit__(self):
        self._days = [self.MON, self.TUE, self.WED, self.THU, self.FRI]

    def __iter__(self):
        return iter(self._days)

cdef int RAND_MAX = 32767

cdef int random_day():
    return rand() % 5 * H_PER_DAY

cdef tuple add_to_plan(list child_plan, int gid, int day, int hour, tuple lesson, list group_subjects):
    if lesson == (0, 0):
        return lesson

    cdef bint teacher_not_free = any([child_plan[gid][day + hour][1] == lesson[1] for gid in range(len(child_plan))])
    if teacher_not_free:
        return 0, 0

    cdef int config_hours = sum([s["hours"] for s in group_subjects if s["id"] == lesson[0]])
    cdef int current_hours = sum([1 if child_plan[gid][i][0] == lesson[0] else 0 for i in range(5 * H_PER_DAY)])
    if current_hours >= config_hours:
        return 0, 0

    return lesson

cdef list fill_plan(list child_plan, int gid, list group_subjects):
    cdef dict subject
    cdef int hours_needed, day, hour, current_hours
    for subject in group_subjects:
        hours_needed = sum([s["hours"] for s in group_subjects if s["id"] == subject["id"]])
        current_hours = sum([1 if child_plan[gid][i][0] == subject["id"] else 0 for i in range(5 * H_PER_DAY)])
        while hours_needed > current_hours:
            day = random_day()
            hour = rand() % H_PER_DAY  # Random hour from 0 to 7
            if child_plan[gid][day + hour] == (0, 0):
                child_plan[gid][day + hour] = (subject["id"], subject["teacher_id"])
                current_hours += 1
    return child_plan

cpdef tuple crossover(list plan1, list plan2, int no_groups, list subjects):
    if plan1 == plan2:
        return None, None

    cdef list child_plan_1 = [[(0, 0) for _ in range((H_PER_DAY * 5))] for _ in range(no_groups)], \
        child_plan_2 = [[(0, 0) for _ in range((H_PER_DAY * 5))] for _ in range(no_groups)]
    cdef int gid, day, hour
    cdef tuple lesson_1, lesson_2
    for gid in range(no_groups):
        for hour in range(H_PER_DAY):
            for day in Day():
                if float(rand() / RAND_MAX) < 0.5:
                    lesson_1, lesson_2 = plan1[gid][day + hour], plan2[gid][day + hour]
                else:
                    lesson_2, lesson_1 = plan1[gid][day + hour], plan2[gid][day + hour]
                child_plan_1[gid][day + hour] = add_to_plan(child_plan_1, gid, day, hour, lesson_1, subjects[gid])
                child_plan_2[gid][day + hour] = add_to_plan(child_plan_2, gid, day, hour, lesson_2, subjects[gid])
    for gid in range(no_groups):
        child_plan_1 = fill_plan(child_plan_1, gid, subjects[gid])
        child_plan_2 = fill_plan(child_plan_2, gid, subjects[gid])
    return child_plan_1, child_plan_2
