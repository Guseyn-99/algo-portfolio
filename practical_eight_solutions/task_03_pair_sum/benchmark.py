
import random
import time
import tracemalloc
import statistics
import multiprocessing as mp

from solutions import (
    pair_nested,
    pair_set,
    pair_dict,
    pair_counter,
    pair_sorted,
    pair_sort,
    pair_bisect,
    pair_adaptive,
)


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


# ==========================================
# 1. Измерение времени
# ==========================================

def time_worker(solution, numbers, target, queue):
    data = numbers.copy()

    start = time.perf_counter()
    result = solution(data, target)
    end = time.perf_counter()

    queue.put((end - start, result))


def measure_time(solution, numbers, target):
    times = []
    expected = pair_set(numbers, target)

    for _ in range(5):
        queue = mp.Queue()

        process = mp.Process(
            target=time_worker,
            args=(solution, numbers, target, queue)
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
            raise RuntimeError("Ошибка процесса замера времени")

        elapsed, result = queue.get(timeout=1)
        queue.close()

        assert result == expected

        if elapsed > 2:
            return "TIMEOUT"

        times.append(elapsed * 1000)

    return f"{statistics.median(times):.4f}"


# ==========================================
# 2. Измерение пиковой памяти
# ==========================================

def memory_worker(solution, numbers, target, queue):
    data = numbers.copy()

    tracemalloc.start()

    result = solution(data, target)

    _, peak = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    queue.put((peak / 1024, result))


def measure_memory(solution, numbers, target):
    queue = mp.Queue()

    process = mp.Process(
        target=memory_worker,
        args=(solution, numbers, target, queue)
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
        raise RuntimeError("Ошибка процесса замера памяти")

    peak, result = queue.get(timeout=1)
    queue.close()

    assert result == pair_set(numbers, target)

    return f"{peak:.4f}"


# ==========================================
# 3. Подсчёт сравнений и вычислений хеша
# ==========================================

class CountedNumber:
    checks = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        CountedNumber.checks += 1
        return self.value < other.value

    def __le__(self, other):
        CountedNumber.checks += 1
        return self.value <= other.value

    def __eq__(self, other):
        CountedNumber.checks += 1
        return self.value == other.value

    def __hash__(self):
        CountedNumber.checks += 1
        return hash(self.value)

    def __add__(self, other):
        return CountedNumber(self.value + other.value)

    def __sub__(self, other):
        return CountedNumber(self.value - other.value)

    def __rsub__(self, other):
        return CountedNumber(other - self.value)


def checks_worker(solution, numbers, target, queue):
    data = [CountedNumber(x) for x in numbers]

    CountedNumber.checks = 0

    result = solution(data, CountedNumber(target))

    queue.put((CountedNumber.checks, result))


def measure_checks(solution, numbers, target):
    queue = mp.Queue()

    process = mp.Process(
        target=checks_worker,
        args=(solution, numbers, target, queue)
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
        raise RuntimeError("Ошибка процесса подсчёта проверок")

    checks, result = queue.get(timeout=1)
    queue.close()

    assert result == pair_set(numbers, target)

    return checks


# ==========================================
# 4. Подготовка данных и запуск эксперимента
# ==========================================

if __name__ == "__main__":
    random.seed(42)

    # 1000 случайных чисел
    small = [
        random.randint(0, 1000000)
        for _ in range(1000)
    ]

    # 100 000 случайных чисел
    large = [
        random.randint(0, 1000000)
        for _ in range(100000)
    ]

    # 100 000 чисел, подходящая пара в конце
    pair_at_end = [
        random.randint(0, 1000000)
        for _ in range(99998)
    ]

    pair_at_end.extend([-7, -3])

    target = -10

    print("Малый набор:", len(small))
    print("Большой набор:", len(large))
    print("Пара в конце:", len(pair_at_end))

    # Замеры времени
    print("\nРезультаты замеров времени (мс):\n")

    for solution in solutions:
        t1 = measure_time(solution, small, target)
        t2 = measure_time(solution, large, target)
        t3 = measure_time(solution, pair_at_end, target)

        print(
            f"{solution.__name__:22} | {t1} | {t2} | {t3}",
            flush=True
        )

    # Замеры памяти
    print("\nПиковая память (КБ):\n")

    for solution in solutions:
        m1 = measure_memory(solution, small, target)
        m2 = measure_memory(solution, large, target)
        m3 = measure_memory(solution, pair_at_end, target)

        print(
            f"{solution.__name__:22} | {m1} | {m2} | {m3}",
            flush=True
        )

    # Подсчёт проверок
    print("\nКоличество проверок:\n")

    for solution in solutions:
        c1 = measure_checks(solution, small, target)
        c2 = measure_checks(solution, large, target)
        c3 = measure_checks(solution, pair_at_end, target)

        print(
            f"{solution.__name__:22} | {c1} | {c2} | {c3}",
            flush=True
        )
