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

cdef list fix_subjects(list plan, list subjects):
    return plan

cdef list fix_teachers(list plan, list teachers):
    return plan

cdef list fix_plan(list plan, list teachers, list subjects): # TODO: do fixing algorithm
    plan = fix_subjects(plan, subjects)
    plan = fix_teachers(plan, subjects)

    return plan