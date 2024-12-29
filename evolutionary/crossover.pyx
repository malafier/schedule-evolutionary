cimport cython
from libc.stdlib cimport rand

cdef int H_PER_DAY = 8

cdef int HOURS = 5 * H_PER_DAY

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

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef tuple crossover(Matrix plan1, Matrix plan2, int no_groups):
    cdef int x, y, dx, dy
    x = rand() % no_groups
    y = rand() % HOURS
    dx = rand() % (no_groups - x)
    dy = rand() % (HOURS - y)

    cdef int row, col, temp
    for row in range(x, x + dx):
        for col in range(y, y + dy):
            temp = plan1[row][col]
            plan1[row][col] = plan2[row][col]
            plan2[row][col] = temp

    return plan1, plan2

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef tuple single_point_crossover(Matrix plan1, Matrix plan2, int no_groups):
    cdef int i, j, temp

    for i in range(len(plan1)):
        for j in range(len(plan1[0])):
            if rand() % 2 == 0:
                temp = plan1[i][j]
                plan1[i][j] = plan2[i][j]
                plan2[i][j] = temp
            else:
                temp = plan2[i][j]
                plan2[i][j] = plan1[i][j]
                plan1[i][j] = temp

    return plan1, plan2
