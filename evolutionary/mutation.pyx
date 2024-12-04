from libc.stdlib cimport rand

cdef int H_PER_DAY = 8

cdef int RAND_MAX = 32767

cdef bool random_direction():
    return rand() % 2 == 1

cdef int random_hour(int no_groups):
    return rand() % (H_PER_DAY * no_groups)

ctypedef list[list[int]] Matrix

cpdef Matrix mutate(Matrix plan, list[dict] subject_to_teacher):
    cdef int i, gid, lesson_h, rows = len(plan), cols = len(plan[0])
    cdef bool left

    # TODO: here get teacher matrix

    for gid in range(rows):
        left = random_direction()
        lesson_h = random_hour(rows)
        while plan[gid][lesson_h] == 0:
            lesson_h = random_hour(rows)

        # TODO: here traverse and search for suitable gap
        # TODO: swap

    return plan