__author__ = 'Omer Ben - Porat'


def solution(A):
    n = len(A)
    left_count, right_count = [0] * n, [0] * n
    left_first, right_first = {}, {}

    total = 0
    for i in xrange(n):
        total += (-1) ** (A[i])
        left_count[i] = total
        if total <= 0:
            if -total not in left_first:
                left_first[-total] = i
    total = 0
    for i in xrange(n - 1, -1, -1):
        total += (-1) ** (A[i] + 1)
        right_count[i] = total
        if total <= 0:
            if -total not in right_first:
                right_first[-total] = i
    res = 0
    for i in xrange(n - 1):
        if left_count[i] > 0:
            start_index= 0
        else:
            if -(left_count[i] - 1) not in left_first or left_first[-(left_count[i] - 1)] >= i:
                continue
            start_index = left_first[-(left_count[i] - 1)] + 1
        if right_count[i + 1] > 0:
            end_index = n - 1
        else:
            if -(right_count[i + 1] - 1) not in right_first or right_first[-(right_count[i + 1] - 1)] <= i + 1:
                continue
            end_index = right_first[-(right_count[i + 1] - 1)] - 1
        res = max(res, end_index - start_index + 1)
    return res