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

cpdef tuple crossover(Matrix plan1, Matrix plan2, int no_groups):
    if plan1 == plan2:
        return None, None

    cdef int x, y, dx, dy
    x = rand() % no_groups
    y = rand() % (5 * H_PER_DAY)
    dx = rand() % (no_groups - x)
    dy = rand() % (5 * H_PER_DAY - y)

    cdef int row, col, temp
    for row in range(x, x+dx):
        for col in range(y, y+dy):
            temp = plan1[row][col]
            plan1[row][col] = plan2[row][col]
            plan2[row][col] = temp

    return plan1, plan2
