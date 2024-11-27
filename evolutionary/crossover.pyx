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

ctypedef list[list[int]] Matrix

cdef int random_x(int no_groups):
    return rand() % no_groups

cdef int random_y():
    return rand() % (5 * H_PER_DAY)

cdef int random_dx(int no_groups, int x):
    return rand() % (no_groups - x)

cdef int random_dy(int y):
    return rand() % (5 * H_PER_DAY - y)


cpdef tuple crossover(Matrix plan1, Matrix plan2, int no_groups):
    if plan1 == plan2:
        return None, None

    cdef int x1, y1, dx, dy
    x1 = random_x(no_groups)
    y1 = random_y()
    dx = random_dx(no_groups, x1)
    dy = random_dy(y1)

    cdef int row, col
    for row in range(x1, x1+dx):
        for col in range(y1, y1+dy):
            plan1[row][col], plan2[row][col] = plan2[row][col], plan1[row][col]

    return plan1, plan2
