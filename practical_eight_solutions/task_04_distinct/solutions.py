
from collections import Counter


# 1. Встроенное множество
def distinct_set(numbers):
    return len(set(numbers))


# 2. Множество с циклом
def distinct_set_loop(numbers):
    seen = set()

    for x in numbers:
        seen.add(x)

    return len(seen)


# 3. Использование словаря
def distinct_dict(numbers):
    seen = {}

    for x in numbers:
        seen[x] = True

    return len(seen)


# 4. Подсчёт частот
def distinct_counter(numbers):
    return len(Counter(numbers))


# 5. Сортировка копии
def distinct_sorted(numbers):
    if not numbers:
        return 0

    data = sorted(numbers)
    count = 1

    for i in range(1, len(data)):
        if data[i] != data[i - 1]:
            count += 1

    return count


# 6. Сортировка исходного списка
def distinct_sort(numbers):
    if not numbers:
        return 0

    numbers.sort()
    count = 1

    for i in range(1, len(numbers)):
        if numbers[i] != numbers[i - 1]:
            count += 1

    return count


# 7. Накопление уникальных чисел в списке
def distinct_list(numbers):
    seen = []

    for x in numbers:
        if x not in seen:
            seen.append(x)

    return len(seen)


# 8. Таблица встреченных значений
def distinct_bytearray(numbers):
    if not numbers:
        return 0

    low = min(numbers)
    high = max(numbers)

    seen = bytearray(high - low + 1)
    count = 0

    for x in numbers:
        index = x - low

        if seen[index] == 0:
            seen[index] = 1
            count += 1

    return count


# Проверка всех решений
if __name__ == "__main__":
    solutions = [
        distinct_set,
        distinct_set_loop,
        distinct_dict,
        distinct_counter,
        distinct_sorted,
        distinct_sort,
        distinct_list,
        distinct_bytearray,
    ]

    tests = [
        ([5, 2, 5, 5, 9, 2], 3),
        ([1, 2, 3, 4], 4),
        ([7, 7, 7], 1),
        ([], 0),
        ([10], 1),
        ([-3, -1, -3, 0], 3),
    ]

    for i, solution in enumerate(solutions, 1):
        for numbers, expected in tests:
            result = solution(numbers.copy())
            assert result == expected

        print(f"{i}. {solution.__name__}: OK")
