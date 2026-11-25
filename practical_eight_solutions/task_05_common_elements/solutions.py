
from bisect import bisect_left


# 1. Пересечение множеств
def common_set(left, right):
    return list(set(left) & set(right))


# 2. Множество с циклом
def common_set_loop(left, right):
    if len(left) > len(right):
        left, right = right, left

    seen = set(left)
    result = []

    for x in right:
        if x in seen:
            result.append(x)
            seen.remove(x)

    return result


# 3. Использование словаря
def common_dict(left, right):
    if len(left) > len(right):
        left, right = right, left

    seen = dict.fromkeys(left)
    result = []

    for x in right:
        if x in seen:
            result.append(x)
            del seen[x]

    return result


# Вспомогательная функция: два указателя
def two_pointers(left, right):
    i = 0
    j = 0
    result = []

    while i < len(left) and j < len(right):
        if left[i] == right[j]:
            if not result or result[-1] != left[i]:
                result.append(left[i])

            i += 1
            j += 1

        elif left[i] < right[j]:
            i += 1

        else:
            j += 1

    return result


# 4. Сортировка копий + два указателя
def common_sorted(left, right):
    return two_pointers(sorted(left), sorted(right))


# 5. Сортировка на месте + два указателя
def common_sort(left, right):
    left.sort()
    right.sort()

    return two_pointers(left, right)


# 6. Бинарный поиск
def common_bisect(left, right):
    data = sorted(right)
    result = set()

    for x in left:
        pos = bisect_left(data, x)

        if pos < len(data) and data[pos] == x:
            result.add(x)

    return list(result)


# 7. Последовательный поиск
def common_list(left, right):
    result = []

    for x in left:
        if x in right and x not in result:
            result.append(x)

    return result


# 8. Таблица встреченных значений
def common_bytearray(left, right):
    if not left or not right:
        return []

    low = max(min(left), min(right))
    high = min(max(left), max(right))

    if low > high:
        return []

    seen = bytearray(high - low + 1)
    result = []

    for x in left:
        if low <= x <= high:
            seen[x - low] = 1

    for x in right:
        if low <= x <= high:
            index = x - low

            if seen[index] == 1:
                result.append(x)
                seen[index] = 0

    return result


# Проверка всех решений
if __name__ == "__main__":
    solutions = [
        common_set,
        common_set_loop,
        common_dict,
        common_sorted,
        common_sort,
        common_bisect,
        common_list,
        common_bytearray,
    ]

    tests = [
        ([1, 2, 2, 4], [2, 2, 3], [2]),
        ([1, 2, 3], [4, 5, 6], []),
        ([1, 2, 3], [3, 2, 1], [1, 2, 3]),
        ([], [1, 2], []),
        ([5, 5, 5], [5, 5], [5]),
        ([-3, -1, 0], [-3, 0, 5], [-3, 0]),
        ([], [], []),
    ]

    for i, solution in enumerate(solutions, 1):
        for left, right, expected in tests:
            result = solution(left.copy(), right.copy())

            assert sorted(result) == sorted(expected)

        print(f"{i}. {solution.__name__}: OK")
