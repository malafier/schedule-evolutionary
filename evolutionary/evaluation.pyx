cimport cython

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

ctypedef list[list[int]] Matrix

cdef bint is_gap(Matrix plan, int gid, int x_day, int start_h, int h_span):
    cdef list lessons = plan[gid][x_day + start_h: x_day + start_h + h_span - 1]
    cdef int lesson_before = plan[gid][x_day + start_h - 1]
    cdef int lesson_after = plan[gid][x_day + start_h + h_span]
    return all(lesson == 0 for lesson in lessons) and lesson_after != 0 and lesson_before != 0

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double gaps_evaluation(Matrix plan):
    cdef int start_h, end_h, gaps, i, gaps_sum  #, day_len_sum
    cdef int groups = len(plan)

    for gid in range(groups):
        for day in Day():
            for i in range(H_PER_DAY):
                if plan[gid][day + i] != 0:
                    start_h = i
                    break
            for i in range(H_PER_DAY - 1, 0, -1):
                if plan[gid][day + i] != 0:
                    end_h = i
                    break

            if start_h >= end_h:
                continue

            gaps = 0
            for i in range(start_h, end_h):
                if plan[gid][day + i] == 0:
                    gaps += 1

            gaps_sum += gaps
            # day_len_sum += end_h - start_h + 1
    return .01 * gaps_sum

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double basic_evaluation(Matrix plan, list[float] weight_per_hour):
    cdef double score = 0
    cdef int i, j, rows = len(plan), cols = len(plan[0])
    cdef tuple lesson
    for gid in range(rows):
        for i in range(cols):
            if plan[gid][i] != 0:
                score += weight_per_hour[i % H_PER_DAY]
    return score

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double hours_per_day_evaluation(Matrix plan):
    cdef double score = 0
    cdef int hours, i
    cdef tuple lesson
    cdef int groups = len(plan)

    for gid in range(groups):
        for day in Day():
            hours = 0
            for i in range(H_PER_DAY):
                if plan[gid][day + i] != 0:
                    hours += 1
            score += 1 if 3 <= hours <= 6 else -hours
    return score

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double max_subject_hours_per_day_evaluation(Matrix plan, list[dict] subjects):
    cdef double score = 0
    cdef int hours, gid, day
    cdef int groups = len(plan)
    cdef dict subject

    for gid in range(groups):
        for day in Day():
            for subject in subjects[gid]:
                hours = 0
                for i in range(H_PER_DAY):
                    if plan[gid][day + i] == subject["id"]:
                        hours += 1
                score += 1 if hours <= 2 else -hours
    return score

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double subject_block_evaluation(Matrix plan, list[dict] subjects):
    cdef double score = 0, reward = 1.0
    cdef list hours
    cdef int day, gid, i, groups = len(plan)
    cdef dict subject

    for gid in range(groups):
        for day in Day():
            for subject in subjects[gid]:
                hours = []
                for i in range(H_PER_DAY):
                    if plan[gid][day + i] == subject["id"]:
                        hours.append(i)
                if len(hours) > 1:
                    for i in range(len(hours) - 1):
                        if hours[i + 1] - hours[i] == 1:
                            score += reward
    return score

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double teacher_block_evaluation(Matrix teacher_plan, list[dict] teachers):
    cdef double score = 0, reward = 1.0
    cdef int teacher_id, day, gid, i, groups = len(teacher_plan)
    cdef list lessons, lesson
    cdef dict teacher

    for teacher in teachers:
        teacher_id = teacher["id"]
        for day in Day():
            lessons = []
            for gid in range(groups):
                for i in range(H_PER_DAY):
                    if teacher_plan[gid][day + i] == teacher_id:
                        lessons.append((gid, i))
            if len(lessons) > 1:
                for i in range(len(lessons) - 1):
                    if lessons[i + 1][1] - lessons[i][1] == 1:
                        score += reward

    return score

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double subject_at_end_or_start_evaluation(Matrix plan, list[dict] subjects):
    cdef double score = 0
    cdef int day, gid, i, first_or_last
    cdef dict subject
    cdef list special_subjects
    cdef int groups = len(plan)

    for gid in range(groups):
        special_subjects = [sub for sub in subjects[gid] if sub["start_end"]]
        for subject in special_subjects:
            for day in Day():
                for i in range(H_PER_DAY):
                    first_or_last = (
                            i == 0 or
                            i == H_PER_DAY - 1 or
                            all([plan[gid][day: day + i] == 0]) or
                            all([plan[gid][day: day + i] == subject["id"]]) or
                            all([plan[gid][day + i + 1: day + H_PER_DAY] == 0]) or
                            all([plan[gid][day + i + 1: day + H_PER_DAY] == subject["id"]])
                    )
                    if plan[gid][day + i] == subject["id"] and first_or_last:
                        score += 1
    return score
