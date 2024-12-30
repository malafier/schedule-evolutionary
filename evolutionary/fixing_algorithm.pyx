from libc.stdlib cimport rand

cdef int H_PER_DAY = 8

cdef int DAYS = 5

cdef int HOURS = DAYS * H_PER_DAY

cdef int RAND_MAX = 32767

cdef int random_day():
    return rand() % 5 * H_PER_DAY

ctypedef list[list[int]] Matrix

cpdef Matrix teacher_matrix(Matrix plan, list[dict] subject_to_teacher):
    cdef int rows = len(plan), cols = HOURS
    cdef Matrix teachers = [[0 for _ in range(cols)] for _ in range(rows)]

    cdef int i, j
    for i in range(rows):
        for j in range(cols):
            if plan[i][j] != 0:
                teachers[i][j] = subject_to_teacher[i][plan[i][j]]

    return teachers

cdef int count_lessons_per_class(list[int] group_plan, int sub):
    cdef int i, count = 0
    for i in range(len(group_plan)):
        if group_plan[i] == sub:
            count += 1
    return count

# Count number of lessons that teacher has on certain hour (should be 0 or 1)
cdef int count_teacher_lessons(Matrix teacher_plan, int teacher, int hour):
    cdef int i, count = 0
    for i in range(len(teacher_plan)):
        if teacher_plan[i][hour] == teacher:
            count += 1
    return count

cdef tuple move_lesson(Matrix plan, Matrix teachers, int lesson, int teacher, int gid):
    cdef int rows = len(plan), cols = HOURS, i = 0, temp_lesson, temp_teacher

    for i in range(cols):
        if plan[gid][i] == 0 and count_teacher_lessons(teachers, teacher, i) == 0:
            plan[gid][i] = lesson
            teachers[gid][i] = teacher
            return plan, teachers

    i = 0
    for i in range(cols):
        if plan[gid][i] != 0 and count_teacher_lessons(teachers, teacher, i) == 0:
            temp_lesson = plan[gid][i]
            temp_teacher = teachers[gid][i]
            plan[gid][i] = lesson
            teachers[gid][i] = teacher
            return move_lesson(plan, teachers, temp_lesson, temp_teacher, gid)

cdef list fix_subjects(Matrix plan, list[list[dict]] subjects):
    cdef int gid, expected_h, actual_h, i, sub_id, rows = len(plan), cols = HOURS
    cdef dict subject

    for gid in range(rows):
        for subject in subjects[gid]:
            expected_h = subject["hours"]
            actual_h = count_lessons_per_class(plan[gid], subject["id"])
            if expected_h == actual_h:
                continue

            sub_id = subject["id"]
            if expected_h < actual_h:
                for i in range(cols):
                    if plan[gid][i] == sub_id:
                        plan[gid][i] = 0
                        actual_h -= 1
                        if expected_h == actual_h:
                            break
                continue

        for subject in subjects[gid]:
            expected_h = subject["hours"]
            actual_h = count_lessons_per_class(plan[gid], subject["id"])
            sub_id = subject["id"]
            if expected_h > actual_h:
                for i in range(cols):
                    if plan[gid][i] == 0:
                        plan[gid][i] = sub_id
                        actual_h += 1
                        if expected_h == actual_h:
                            break
    return plan

cdef list fix_teachers(Matrix plan, Matrix teachers):
    cdef int i, j, rows = len(plan), cols = HOURS, cur_teach, lesson

    for i in range(rows):
        for j in range(cols):
            cur_teach = teachers[i][j]
            if cur_teach == 0 or count_teacher_lessons(teachers, cur_teach, j) < 2:
                continue

            lesson = plan[i][j]
            plan[i][j] = 0
            teachers[i][j] = 0
            plan, teachers = move_lesson(plan, teachers, lesson, cur_teach, i)
    return plan

cpdef list fix_plan(Matrix plan, list[list[dict]] subjects, list[dict] subject_to_teacher):
    plan = fix_subjects(plan, subjects)

    teachers = teacher_matrix(plan, subject_to_teacher)
    plan = fix_teachers(plan, teachers)

    return plan

cpdef list fix_late_gaps(Matrix plan, list[dict] subject_to_teacher):
    cdef int i, day, last_lesson, rows = len(plan), temp

    teachers = teacher_matrix(plan, subject_to_teacher)

    for i in range(rows):
        for day in range(DAYS):
            # Index of last lesson of the day
            last_lesson = (day + 1) * H_PER_DAY - 1

            # Find gap lesson that is after 5-th hour
            while plan[i][last_lesson] == 0 and last_lesson % H_PER_DAY > 5:
                last_lesson -= 1

            # Skip if lesson is still a gap or 2 lessons before are not gaps
            if plan[i][last_lesson] == 0 or (plan[i][last_lesson - 1] != 0 and plan[i][last_lesson - 2] != 0):
                continue

            # Check if previous plan is a gap
            # if true check, if swapping lessons would create teacher conflict
            # if true, move lesson and teacher
            if plan[i][last_lesson - 1] == 0 \
                    and count_teacher_lessons(teachers, teachers[i][last_lesson], last_lesson - 1) == 0:
                plan[i][last_lesson - 1] = plan[i][last_lesson]
                plan[i][last_lesson] = 0

                teachers[i][last_lesson - 1] = teachers[i][last_lesson]
                plan[i][last_lesson] = 0
                continue

            # If previous wasn't moved by one try the same with lesson before
            if plan[i][last_lesson - 2] == 0 \
                    and count_teacher_lessons(teachers, teachers[i][last_lesson], last_lesson - 2) == 0:
                plan[i][last_lesson - 2] = plan[i][last_lesson]
                plan[i][last_lesson] = 0

                teachers[i][last_lesson - 2] = teachers[i][last_lesson]
                plan[i][last_lesson] = 0

    return plan
