
from collections import Counter
from bisect import bisect_left


# 1. Сравнение размеров списка и множества
def duplicate_set(numbers):
    return len(numbers) != len(set(numbers))


# 2. Множество с ранним выходом
def duplicate_set_loop(numbers):
    seen = set()

    for x in numbers:
        if x in seen:
            return True
        seen.add(x)

    return False


# 3. Использование словаря
def duplicate_dict(numbers):
    seen = {}

    for x in numbers:
        if x in seen:
            return True
        seen[x] = True

    return False


# 4. Подсчёт частоты элементов
def duplicate_counter(numbers):
    counts = Counter(numbers)
    return any(count > 1 for count in counts.values())


# 5. Сортировка копии
def duplicate_sorted(numbers):
    data = sorted(numbers)

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            return True

    return False


# 6. Сортировка исходного списка
def duplicate_sort(numbers):
    numbers.sort()

    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i - 1]:
            return True

    return False


# 7. Два вложенных цикла
def duplicate_nested(numbers):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j]:
                return True

    return False


# 8. Бинарный поиск
def duplicate_bisect(numbers):
    seen = []

    for x in numbers:
        pos = bisect_left(seen, x)

        if pos < len(seen) and seen[pos] == x:
            return True

        seen.insert(pos, x)

    return False


# Проверка решений
if __name__ == "__main__":
    solutions = [
        duplicate_set,
        duplicate_set_loop,
        duplicate_dict,
        duplicate_counter,
        duplicate_sorted,
        duplicate_sort,
        duplicate_nested,
        duplicate_bisect,
    ]

    tests = [
        ([4, 9, 2, 9], True),
        ([1, 2, 3, 4], False),
        ([], False),
        ([5], False),
        ([7, 7], True),
    ]

    for i, solution in enumerate(solutions, 1):
        for numbers, expected in tests:
            result = solution(numbers.copy())
            assert result == expected

        print(f"{i}. {solution.__name__}: OK")
