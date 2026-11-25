
from itertools import groupby


# 1. Один проход по индексам
def max_run_index(numbers):
    if not numbers:
        return 0

    current = 1
    best = 1

    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i - 1]:
            current += 1
        else:
            current = 1

        if current > best:
            best = current

    return best


# 2. Один проход через итератор
def max_run_iterator(numbers):
    if not numbers:
        return 0

    iterator = iter(numbers)
    previous = next(iterator)

    current = 1
    best = 1

    for x in iterator:
        if x == previous:
            current += 1
        else:
            current = 1

        if current > best:
            best = current

        previous = x

    return best


# 3. Два указателя
def max_run_pointers(numbers):
    left = 0
    best = 0
    n = len(numbers)

    while left < n:
        right = left + 1

        while right < n and numbers[right] == numbers[left]:
            right += 1

        best = max(best, right - left)
        left = right

    return best


# 4. Группировка через groupby
def max_run_groupby(numbers):
    return max(
        (sum(1 for _ in group) for _, group in groupby(numbers)),
        default=0
    )


# 5. Динамическое программирование
def max_run_dp(numbers):
    if not numbers:
        return 0

    dp = [1] * len(numbers)

    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i - 1]:
            dp[i] = dp[i - 1] + 1

    return max(dp)


# 6. Сравнение соседних элементов через zip
def max_run_zip(numbers):
    if not numbers:
        return 0

    current = 1
    best = 1

    for a, b in zip(numbers, numbers[1:]):
        if a == b:
            current += 1
        else:
            current = 1

        if current > best:
            best = current

    return best


# 7. Вложенные циклы
def max_run_nested(numbers):
    best = 0
    n = len(numbers)

    for i in range(n):
        current = 1

        for j in range(i + 1, n):
            if numbers[j] != numbers[i]:
                break

            current += 1

        if current > best:
            best = current

    return best


# 8. Разделяй и властвуй
def max_run_divide(numbers):
    if not numbers:
        return 0

    def solve(left, right):
        if right - left == 1:
            return 1, 1, 1

        mid = (left + right) // 2

        left_best, left_prefix, left_suffix = solve(left, mid)
        right_best, right_prefix, right_suffix = solve(mid, right)

        best = max(left_best, right_best)
        prefix = left_prefix
        suffix = right_suffix

        if numbers[mid - 1] == numbers[mid]:
            best = max(best, left_suffix + right_prefix)

            if left_prefix == mid - left:
                prefix = left_prefix + right_prefix

            if right_suffix == right - mid:
                suffix = right_suffix + left_suffix

        return best, prefix, suffix

    return solve(0, len(numbers))[0]


# Проверка всех решений
if __name__ == "__main__":
    solutions = [
        max_run_index,
        max_run_iterator,
        max_run_pointers,
        max_run_groupby,
        max_run_dp,
        max_run_zip,
        max_run_nested,
        max_run_divide,
    ]

    tests = [
        ([1, 1, 2, 2, 2, 3], 3),
        ([], 0),
        ([5], 1),
        ([7, 7, 7, 7], 4),
        ([1, 2, 3, 4], 1),
        ([1, 1, 1, 2, 3], 3),
        ([1, 2, 3, 3, 3], 3),
        ([1, 1, 2, 1, 1], 2),
        ([-2, -2, -2, 0], 3),
    ]

    for i, solution in enumerate(solutions, 1):
        for numbers, expected in tests:
            result = solution(numbers.copy())
            assert result == expected

        print(f"{i}. {solution.__name__}: OK")
