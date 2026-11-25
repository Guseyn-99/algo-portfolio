
# 1. Математическая формула суммы
def missing_sum(ids, n):
    return n * (n + 1) // 2 - sum(ids)


# 2. Побитовая операция XOR
def missing_xor(ids, n):
    result = n

    for i, x in enumerate(ids):
        result ^= i ^ x

    return result


# 3. Использование множества
def missing_set(ids, n):
    seen = set(ids)

    for x in range(n + 1):
        if x not in seen:
            return x


# 4. Сортировка копии списка
def missing_sorted(ids, n):
    data = sorted(ids)

    for i, x in enumerate(data):
        if i != x:
            return i

    return n


# 5. Сортировка исходного списка
def missing_sort(ids, n):
    ids.sort()

    for i, x in enumerate(ids):
        if i != x:
            return i

    return n


# 6. Таблица встреченных чисел
def missing_bytearray(ids, n):
    seen = bytearray(n + 1)

    for x in ids:
        seen[x] = 1

    for i in range(n + 1):
        if seen[i] == 0:
            return i


# 7. Последовательный поиск
def missing_list(ids, n):
    for x in range(n + 1):
        if x not in ids:
            return x


# 8. Циклическая сортировка
def missing_cyclic(ids, n):
    i = 0

    while i < n:
        x = ids[i]

        if x < n and x != i:
            ids[i], ids[x] = ids[x], ids[i]
        else:
            i += 1

    for i, x in enumerate(ids):
        if i != x:
            return i

    return n


# Проверка всех решений
if __name__ == "__main__":
    solutions = [
        missing_sum,
        missing_xor,
        missing_set,
        missing_sorted,
        missing_sort,
        missing_bytearray,
        missing_list,
        missing_cyclic,
    ]

    tests = [
        ([3, 0, 1], 3, 2),
        ([1, 2, 3], 3, 0),
        ([0, 1, 2], 3, 3),
        ([4, 2, 0, 1], 4, 3),
        ([0], 1, 1),
        ([1], 1, 0),
        ([], 0, 0),
    ]

    for i, solution in enumerate(solutions, 1):
        for ids, n, expected in tests:
            result = solution(ids.copy(), n)
            assert result == expected

        print(f"{i}. {solution.__name__}: OK")
