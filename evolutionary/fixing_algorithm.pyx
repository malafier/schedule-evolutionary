from libc.stdlib cimport rand

cdef int H_PER_DAY = 8

cdef int RAND_MAX = 32767

cdef int random_day():
    return rand() % 5 * H_PER_DAY

ctypedef list[list[int]] Matrix

cpdef Matrix teacher_matrix(Matrix plan, list[dict] subject_to_teacher):
    cdef int rows = len(plan), cols = len(plan[0])
    cdef Matrix teachers = [[0 for _ in range(cols)] for _ in range(rows)]

    cdef i, j
    for i in range(rows):
        for j in range(cols):
            teachers[i][j] = 0 if plan[i][j] == 0 else subject_to_teacher[i][plan[i][j]]

    return teachers

cdef list fix_subjects(Matrix plan, list[dict] subjects):
    return plan

cdef list fix_teachers(Matrix plan, list[dict] teachers):
    return plan

cpdef list fix_plan(Matrix plan, list[dict] subjects, list[dict] subject_to_teacher): # TODO: do fixing algorithm
    teachers = teacher_matrix(plan, subject_to_teacher)

    plan = fix_subjects(plan, subjects)
    plan = fix_teachers(plan, teachers)

    return plan
