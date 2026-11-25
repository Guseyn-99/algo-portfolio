
import random
import time
import tracemalloc
import statistics
import multiprocessing as mp

from solutions import (
    missing_sum,
    missing_xor,
    missing_set,
    missing_sorted,
    missing_sort,
    missing_bytearray,
    missing_list,
    missing_cyclic,
)


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


# 1. Измерение времени

def time_worker(solution, ids, n, queue):
    data = ids.copy()

    start = time.perf_counter()
    result = solution(data, n)
    elapsed = time.perf_counter() - start

    queue.put((elapsed, result))


def measure_time(solution, ids, n):
    times = []
    expected = missing_sum(ids, n)

    for _ in range(5):
        queue = mp.Queue()

        process = mp.Process(
            target=time_worker,
            args=(solution, ids, n, queue)
        )

        process.start()
        process.join(timeout=2)

        if process.is_alive():
            process.terminate()
            process.join()
            queue.close()
            return "TIMEOUT"

        if process.exitcode != 0:
            queue.close()
            raise RuntimeError("Ошибка замера времени")

        elapsed, result = queue.get(timeout=1)
        queue.close()

        assert result == expected

        if elapsed > 2:
            return "TIMEOUT"

        times.append(elapsed * 1000)

    return f"{statistics.median(times):.4f}"


# 2. Измерение пиковой памяти

def memory_worker(solution, ids, n, queue):
    data = ids.copy()

    tracemalloc.start()

    result = solution(data, n)

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    queue.put((peak / 1024, result))


def measure_memory(solution, ids, n):
    queue = mp.Queue()

    process = mp.Process(
        target=memory_worker,
        args=(solution, ids, n, queue)
    )

    process.start()
    process.join(timeout=2)

    if process.is_alive():
        process.terminate()
        process.join()
        queue.close()
        return "TIMEOUT"

    if process.exitcode != 0:
        queue.close()
        raise RuntimeError("Ошибка замера памяти")

    peak, result = queue.get(timeout=1)
    queue.close()

    assert result == missing_sum(ids, n)

    return f"{peak:.4f}"


# 3. Подсчёт проверок

class CountedNumber:
    checks = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        CountedNumber.checks += 1
        return self.value < other.value

    def __eq__(self, other):
        CountedNumber.checks += 1

        if isinstance(other, CountedNumber):
            return self.value == other.value

        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        CountedNumber.checks += 1
        return hash(self.value)


def counted_solution(solution, ids, n):
    checks = 0

    # Формула суммы не сравнивает значения
    if solution == missing_sum:
        return 0, missing_sum(ids, n)

    # XOR не сравнивает значения
    if solution == missing_xor:
        return 0, missing_xor(ids, n)

    # Таблица встреченных чисел
    if solution == missing_bytearray:
        seen = bytearray(n + 1)

        for x in ids:
            seen[x] = 1

        for i in range(n + 1):
            checks += 1

            if seen[i] == 0:
                return checks, i

    # Циклическая сортировка
    if solution == missing_cyclic:
        data = ids.copy()
        i = 0

        while i < n:
            x = data[i]

            checks += 1

            if x < n:
                checks += 1

                if x != i:
                    data[i], data[x] = data[x], data[i]
                    continue

            i += 1

        for i, x in enumerate(data):
            checks += 1

            if i != x:
                return checks, i

        return checks, n

    # Остальные алгоритмы
    data = [CountedNumber(x) for x in ids]
    CountedNumber.checks = 0

    if solution == missing_set:
        seen = set(data)

        for x in range(n + 1):
            if CountedNumber(x) not in seen:
                return CountedNumber.checks, x

    result = solution(data, n)

    return CountedNumber.checks, result


def checks_worker(solution, ids, n, queue):
    checks, result = counted_solution(solution, ids, n)

    queue.put((checks, result))


def measure_checks(solution, ids, n):
    queue = mp.Queue()

    process = mp.Process(
        target=checks_worker,
        args=(solution, ids, n, queue)
    )

    process.start()
    process.join(timeout=2)

    if process.is_alive():
        process.terminate()
        process.join()
        queue.close()
        return "TIMEOUT"

    if process.exitcode != 0:
        queue.close()
        raise RuntimeError("Ошибка подсчёта проверок")

    checks, result = queue.get(timeout=1)
    queue.close()

    assert result == missing_sum(ids, n)

    return checks


# 4. Подготовка данных

def generate_ids(n, missing):
    ids = list(range(n + 1))
    ids.remove(missing)
    random.shuffle(ids)

    return ids


if __name__ == "__main__":
    random.seed(42)

    # Перемешанные списки
    small = generate_ids(1000, 500)
    large = generate_ids(100000, 50000)

    # Пропущено первое число диапазона
    missing_at_start = generate_ids(100000, 0)

    datasets = [
        (small, 1000),
        (large, 100000),
        (missing_at_start, 100000),
    ]

    print("Малый набор:", len(small))
    print("Большой набор:", len(large))
    print("Пропуск в начале:", len(missing_at_start))

    print("\nПропущенные числа:")

    for ids, n in datasets:
        print(missing_sum(ids, n))

    # Замеры времени
    print("\nРезультаты замеров времени (мс):\n")

    for solution in solutions:
        values = [
            measure_time(solution, ids, n)
            for ids, n in datasets
        ]

        print(
            f"{solution.__name__:22} | "
            + " | ".join(map(str, values)),
            flush=True
        )

    # Замеры памяти
    print("\nПиковая память (КБ):\n")

    for solution in solutions:
        values = [
            measure_memory(solution, ids, n)
            for ids, n in datasets
        ]

        print(
            f"{solution.__name__:22} | "
            + " | ".join(map(str, values)),
            flush=True
        )

    # Подсчёт проверок
    print("\nКоличество проверок:\n")

    for solution in solutions:
        values = [
            measure_checks(solution, ids, n)
            for ids, n in datasets
        ]

        print(
            f"{solution.__name__:22} | "
            + " | ".join(map(str, values)),
            flush=True
        )
