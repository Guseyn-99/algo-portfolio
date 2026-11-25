
import random
import time
import tracemalloc
import statistics
import multiprocessing as mp

from solutions import (
    common_set,
    common_set_loop,
    common_dict,
    common_sorted,
    common_sort,
    common_bisect,
    common_list,
    common_bytearray,
)


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


# 1. Измерение времени

def time_worker(solution, left, right, queue):
    a = left.copy()
    b = right.copy()

    start = time.perf_counter()
    result = solution(a, b)
    elapsed = time.perf_counter() - start

    correct = sorted(result) == sorted(set(left) & set(right))

    queue.put((elapsed, correct))


def measure_time(solution, left, right):
    times = []

    for _ in range(5):
        queue = mp.Queue()

        process = mp.Process(
            target=time_worker,
            args=(solution, left, right, queue)
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

        elapsed, correct = queue.get(timeout=1)
        queue.close()

        assert correct

        if elapsed > 2:
            return "TIMEOUT"

        times.append(elapsed * 1000)

    return f"{statistics.median(times):.4f}"


# 2. Измерение пиковой памяти

def memory_worker(solution, left, right, queue):
    a = left.copy()
    b = right.copy()

    tracemalloc.start()

    result = solution(a, b)

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    correct = sorted(result) == sorted(set(left) & set(right))

    queue.put((peak / 1024, correct))


def measure_memory(solution, left, right):
    queue = mp.Queue()

    process = mp.Process(
        target=memory_worker,
        args=(solution, left, right, queue)
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

    peak, correct = queue.get(timeout=1)
    queue.close()

    assert correct

    return f"{peak:.4f}"


# 3. Подсчёт проверок

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

    def __gt__(self, other):
        CountedNumber.checks += 1
        return self.value > other.value

    def __ge__(self, other):
        CountedNumber.checks += 1
        return self.value >= other.value

    def __eq__(self, other):
        CountedNumber.checks += 1
        return self.value == other.value

    def __ne__(self, other):
        CountedNumber.checks += 1
        return self.value != other.value

    def __hash__(self):
        CountedNumber.checks += 1
        return hash(self.value)

    def __sub__(self, other):
        return self.value - other.value


# Отдельный подсчёт проверок для bytearray
def counted_bytearray(left, right):
    if not left or not right:
        return 0, []

    a = [CountedNumber(x) for x in left]
    b = [CountedNumber(x) for x in right]

    CountedNumber.checks = 0

    low = max(min(a), min(b))
    high = min(max(a), max(b))

    if low > high:
        return CountedNumber.checks, []

    seen = bytearray(high - low + 1)
    result = []

    for x in a:
        if low <= x <= high:
            seen[x - low] = 1

    for x in b:
        if low <= x <= high:
            index = x - low

            CountedNumber.checks += 1

            if seen[index] == 1:
                result.append(x.value)
                seen[index] = 0

    return CountedNumber.checks, result


def checks_worker(solution, left, right, queue):
    if solution == common_bytearray:
        checks, result = counted_bytearray(left, right)
    else:
        a = [CountedNumber(x) for x in left]
        b = [CountedNumber(x) for x in right]

        CountedNumber.checks = 0

        result = solution(a, b)

        checks = CountedNumber.checks
        result = [x.value for x in result]

    correct = sorted(result) == sorted(set(left) & set(right))

    queue.put((checks, correct))


def measure_checks(solution, left, right):
    queue = mp.Queue()

    process = mp.Process(
        target=checks_worker,
        args=(solution, left, right, queue)
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

    checks, correct = queue.get(timeout=1)
    queue.close()

    assert correct

    return checks


# 4. Подготовка данных и запуск

if __name__ == "__main__":
    random.seed(42)

    # Два списка по 1000 чисел
    small_left = [
        random.randint(0, 1000000)
        for _ in range(1000)
    ]

    small_right = [
        random.randint(0, 1000000)
        for _ in range(1000)
    ]

    # Два списка по 100 000 чисел
    large_left = [
        random.randint(0, 1000000)
        for _ in range(100000)
    ]

    large_right = [
        random.randint(0, 1000000)
        for _ in range(100000)
    ]

    # Два отсортированных списка
    sorted_left = sorted(large_left)
    sorted_right = sorted(large_right)

    datasets = [
        (small_left, small_right),
        (large_left, large_right),
        (sorted_left, sorted_right),
    ]

    print("Малые списки:", len(small_left), len(small_right))
    print("Большие списки:", len(large_left), len(large_right))
    print("Отсортированные:", len(sorted_left), len(sorted_right))

    print("\nКоличество общих чисел:")

    for left, right in datasets:
        print(len(set(left) & set(right)))

    # Замеры времени
    print("\nРезультаты замеров времени (мс):\n")

    for solution in solutions:
        values = [
            measure_time(solution, left, right)
            for left, right in datasets
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
            measure_memory(solution, left, right)
            for left, right in datasets
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
            measure_checks(solution, left, right)
            for left, right in datasets
        ]

        print(
            f"{solution.__name__:22} | "
            + " | ".join(map(str, values)),
            flush=True
        )
