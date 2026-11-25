
from collections import Counter
from array import array


# 1. Подсчёт частот через словарь
def frequent_dict(numbers):
    counts = {}

    for x in numbers:
        counts[x] = counts.get(x, 0) + 1

    best = numbers[0]
    best_count = 0

    for x, count in counts.items():
        if count > best_count or (
            count == best_count and x < best
        ):
            best = x
            best_count = count

    return best


# 2. Использование Counter
def frequent_counter(numbers):
    counts = Counter(numbers)

    best = numbers[0]
    best_count = 0

    for x, count in counts.items():
        if count > best_count or (
            count == best_count and x < best
        ):
            best = x
            best_count = count

    return best


# 3. Словарь с обновлением лидера
def frequent_online(numbers):
    counts = {}
    best = numbers[0]
    best_count = 0

    for x in numbers:
        counts[x] = counts.get(x, 0) + 1
        count = counts[x]

        if count > best_count or (
            count == best_count and x < best
        ):
            best = x
            best_count = count

    return best


# Подсчёт серий в отсортированном списке
def scan_sorted(numbers):
    best = numbers[0]
    best_count = 1
    current = 1

    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i - 1]:
            current += 1
        else:
            current = 1

        if current > best_count:
            best = numbers[i]
            best_count = current

    return best


# 4. Сортировка копии списка
def frequent_sorted(numbers):
    return scan_sorted(sorted(numbers))


# 5. Сортировка на месте
def frequent_sort(numbers):
    numbers.sort()

    return scan_sorted(numbers)


# 6. Таблица частот
def frequent_array(numbers):
    low = min(numbers)
    high = max(numbers)

    counts = array("I", [0]) * (high - low + 1)

    for x in numbers:
        counts[x - low] += 1

    best_index = 0
    best_count = 0

    for i, count in enumerate(counts):
        if count > best_count:
            best_index = i
            best_count = count

    return low + best_index


# 7. Последовательный подсчёт частот
def frequent_count(numbers):
    best = numbers[0]
    best_count = 0

    for x in numbers:
        count = numbers.count(x)

        if count > best_count or (
            count == best_count and x < best
        ):
            best = x
            best_count = count

    return best


# 8. Множество и подсчёт частот
def frequent_set_count(numbers):
    best = numbers[0]
    best_count = 0

    for x in set(numbers):
        count = numbers.count(x)

        if count > best_count or (
            count == best_count and x < best
        ):
            best = x
            best_count = count

    return best


# Проверка всех решений
if __name__ == "__main__":
    solutions = [
        frequent_dict,
        frequent_counter,
        frequent_online,
        frequent_sorted,
        frequent_sort,
        frequent_array,
        frequent_count,
        frequent_set_count,
    ]

    tests = [
        ([3, 1, 3, 2, 2, 2], 2),
        ([5, 5, 2, 2], 2),
        ([7], 7),
        ([4, 4, 4], 4),
        ([5, 3, 1, 2], 1),
        ([-3, -3, -1, -1], -3),
        ([0, 1, 0, 2], 0),
        ([1, 2, 3, 3, 2, 2], 2),
        ([9, 9, 1, 1, 9, 1], 1),
    ]

    for i, solution in enumerate(solutions, 1):
        for numbers, expected in tests:
            result = solution(numbers.copy())
            assert result == expected

        print(f"{i}. {solution.__name__}: OK")
