cimport cython
from libc.stdlib cimport rand

ctypedef list[list[int]] Matrix

cdef int H_PER_DAY = 8

cdef int HOURS = 5 * H_PER_DAY

cdef int RAND_MAX = 32767

cdef list[int] PREFERRED_HOURS = [2, 3, 4, 5, 10, 11, 12, 13, 18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37]

cdef list[int] OTHER_HOURS = [0, 1, 6, 7, 8, 9, 14, 15, 16, 17, 22, 23, 24, 25, 30, 31, 32, 33, 38, 39]

cdef int random_hour():
    return rand() % HOURS

@cython.boundscheck(False)
@cython.wraparound(False)
cdef list[int] shuffle(list[int] arr):
    cdef int n = len(arr)
    cdef int i, j

    for i in range(n-1, 0, -1):
        j = rand() % (i + 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

@cython.boundscheck(False)
@cython.wraparound(False)
cdef Matrix teacher_matrix(Matrix plan, list[dict] subject_to_teacher):
    cdef int rows = len(plan), cols = HOURS
    cdef Matrix teachers = [[0 for _ in range(cols)] for _ in range(rows)]

    cdef int i, j
    for i in range(rows):
        for j in range(cols):
            teachers[i][j] = 0 if plan[i][j] == 0 else subject_to_teacher[i][plan[i][j]]

    return teachers

@cython.boundscheck(False)
@cython.wraparound(False)
cdef int count_teacher_lessons(Matrix teacher_plan, int teacher, int hour):
    cdef int i, count = 0
    for i in range(len(teacher_plan)):
        if teacher_plan[i][hour] == teacher:
            count += 1
    return count

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Matrix mutate(Matrix plan, list[dict] subject_to_teacher):
    cdef int i, gid, lesson_h, rows = len(plan), cols = HOURS, temp
    cdef int mutated = 0

    teachers = teacher_matrix(plan, subject_to_teacher)
    cdef list[int] pref_hours = shuffle(PREFERRED_HOURS), other_hours = shuffle(OTHER_HOURS)

    for gid in range(rows):
        lesson_h = random_hour()
        while plan[gid][lesson_h] == 0:
            lesson_h = random_hour()

        for i in pref_hours:
            if count_teacher_lessons(teachers, teachers[gid][lesson_h], i) == 0 and plan[gid][i] == 0:
                plan[gid][i] = plan[gid][lesson_h]
                teachers[gid][i] = teachers[gid][lesson_h]
                plan[gid][lesson_h] = 0
                teachers[gid][lesson_h] = 0
                mutated = 1
                break
        if mutated == 1:
            continue

        for i in other_hours:
            if count_teacher_lessons(teachers, teachers[gid][lesson_h], i) == 0 and plan[gid][i] == 0:
                plan[gid][i] = plan[gid][lesson_h]
                teachers[gid][i] = teachers[gid][lesson_h]
                plan[gid][lesson_h] = 0
                teachers[gid][lesson_h] = 0
                mutated = 1
                break
        if mutated == 1:
            continue

        for i in range(HOURS):
            if count_teacher_lessons(teachers, teachers[gid][lesson_h], i) == 0 \
                    and count_teacher_lessons(teachers, teachers[gid][i], lesson_h) == 0:
                temp = plan[gid][i]
                plan[gid][i] = plan[gid][lesson_h]
                plan[gid][lesson_h] = temp

                temp = teachers[gid][i]
                teachers[gid][i] = teachers[gid][lesson_h]
                teachers[gid][lesson_h] = temp
                break

    return plan