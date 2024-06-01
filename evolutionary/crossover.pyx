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

cdef tuple add_to_plan(dict child_plan, str group, int day, int hour, tuple lesson, list group_subjects):
    if lesson == (0, 0):
        return lesson

    cdef bint teacher_free = any([child_plan[g][day + hour][1] != lesson[1] for g in child_plan.keys()])
    if not teacher_free:
        return 0, 0

    cdef int config_hours = sum([s["hours"] for s in group_subjects if s["id"] == lesson[0]])
    cdef int current_hours = sum([1 if child_plan[group][i][0] == lesson[0] else 0 for i in range(5 * H_PER_DAY)])
    if current_hours >= config_hours:
        return 0, 0

    return lesson

cdef dict fill_plan(dict child_plan, str group, list group_subjects):
    cdef dict subject
    cdef int hours_needed, day, hour
    for subject in group_subjects:
        hours_needed = sum([s["hours"] for s in group_subjects if s["id"] == subject["id"]])
        while hours_needed > sum([1 if child_plan[group][i][0] == subject["id"] else 0 for i in range(5 * H_PER_DAY)]):
            day = random_day()
            hour = rand() % H_PER_DAY  # Random hour from 0 to 7
            if child_plan[group][day + hour] == (0, 0):
                child_plan[group][day + hour] = (subject["id"], subject["teacher_id"])
    return child_plan

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef dict single_point_cross(dict plan1, dict plan2, list groups, dict subjects):
    if plan1 == plan2:
        return None

    cdef dict child_plan = {class_name: [(0, 0) for _ in range((H_PER_DAY * 5))] for class_name in groups}
    cdef str name
    cdef int day
    cdef int hour
    cdef tuple lesson
    for name in groups:
        for day in Day():
            for hour in range(H_PER_DAY):
                if float(rand() / RAND_MAX) < 0.5:
                    lesson = plan2[name][day + hour]
                else:
                    lesson = plan1[name][day + hour]
                child_plan[name][day + hour] = add_to_plan(child_plan, name, day, hour, lesson, subjects[name])
    for group in groups:
        child_plan = fill_plan(child_plan, group, subjects[group])
    return child_plan

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef dict day_cross(dict plan1, dict plan2, list groups, dict subjects):
    if plan1 == plan2:
        return None

    cdef dict child_plan = {class_name: [(0, 0) for _ in range((H_PER_DAY * 5))] for class_name in groups}
    cdef str name
    cdef int day, hour
    cdef dict plan
    cdef tuple lesson
    for name in groups:
        for day in Day():
            if float(rand() / RAND_MAX) < 0.5:
                plan = plan2
            else:
                plan = plan1
            for hour in range(H_PER_DAY):
                lesson = plan[name][day + hour]
                child_plan[name][day + hour] = add_to_plan(child_plan, name, day, hour, lesson, subjects[name])
    for group in groups:
        child_plan = fill_plan(child_plan, group, subjects[group])
    return child_plan
