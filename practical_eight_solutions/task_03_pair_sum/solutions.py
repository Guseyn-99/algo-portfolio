
from collections import Counter
from bisect import bisect_left


# 1. Два вложенных цикла
def pair_nested(numbers, target):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return True

    return False


# 2. Использование множества
def pair_set(numbers, target):
    seen = set()

    for x in numbers:
        if target - x in seen:
            return True

        seen.add(x)

    return False


# 3. Использование словаря
def pair_dict(numbers, target):
    seen = {}

    for i, x in enumerate(numbers):
        if target - x in seen:
            return True

        seen[x] = i

    return False


# 4. Подсчёт частот
def pair_counter(numbers, target):
    counts = Counter(numbers)

    for x in counts:
        need = target - x

        if need in counts:
            if need != x or counts[x] >= 2:
                return True

    return False


# Вспомогательная функция: два указателя
def two_pointers(numbers, target):
    left = 0
    right = len(numbers) - 1

    while left < right:
        total = numbers[left] + numbers[right]

        if total == target:
            return True

        if total < target:
            left += 1
        else:
            right -= 1

    return False


# 5. Сортировка копии + два указателя
def pair_sorted(numbers, target):
    data = sorted(numbers)
    return two_pointers(data, target)


# 6. Сортировка на месте + два указателя
def pair_sort(numbers, target):
    numbers.sort()
    return two_pointers(numbers, target)


# 7. Сортировка + бинарный поиск
def pair_bisect(numbers, target):
    data = sorted(numbers)

    for i, x in enumerate(data):
        need = target - x
        pos = bisect_left(data, need, i + 1)

        if pos < len(data) and data[pos] == need:
            return True

    return False


# 8. Проверка сортировки + два указателя
def pair_adaptive(numbers, target):
    is_sorted = all(
        numbers[i] <= numbers[i + 1]
        for i in range(len(numbers) - 1)
    )

    if not is_sorted:
        numbers.sort()

    return two_pointers(numbers, target)


# Проверка всех решений
if __name__ == "__main__":
    solutions = [
        pair_nested,
        pair_set,
        pair_dict,
        pair_counter,
        pair_sorted,
        pair_sort,
        pair_bisect,
        pair_adaptive,
    ]

    tests = [
        ([2, 7, 11, 15], 9, True),
        ([1, 2, 3], 10, False),
        ([5], 10, False),
        ([5, 5], 10, True),
        ([], 0, False),
        ([-3, 4, 7], 1, True),
        ([0, 0], 0, True),
    ]

    for i, solution in enumerate(solutions, 1):
        for numbers, target, expected in tests:
            result = solution(numbers.copy(), target)
            assert result == expected

        print(f"{i}. {solution.__name__}: OK")
