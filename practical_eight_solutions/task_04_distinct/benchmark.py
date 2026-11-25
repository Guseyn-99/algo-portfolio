
import random
import time
import tracemalloc
import statistics
import multiprocessing as mp

from solutions import (
    distinct_set,
    distinct_set_loop,
    distinct_dict,
    distinct_counter,
    distinct_sorted,
    distinct_sort,
    distinct_list,
    distinct_bytearray,
)


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


# 1. Измерение времени

def time_worker(solution, numbers, queue):
    data = numbers.copy()

    start = time.perf_counter()
    result = solution(data)
    end = time.perf_counter()

    queue.put((end - start, result))


def measure_time(solution, numbers):
    times = []
    expected = len(set(numbers))

    for _ in range(5):
        queue = mp.Queue()

        process = mp.Process(
            target=time_worker,
            args=(solution, numbers, queue)
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

def memory_worker(solution, numbers, queue):
    data = numbers.copy()

    tracemalloc.start()
    result = solution(data)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    queue.put((peak / 1024, result))


def measure_memory(solution, numbers):
    queue = mp.Queue()

    process = mp.Process(
        target=memory_worker,
        args=(solution, numbers, queue)
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

    assert result == len(set(numbers))

    return f"{peak:.4f}"


# 3. Подсчёт проверок

class CountedNumber:
    checks = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        CountedNumber.checks += 1
        return self.value < other.value

    def __gt__(self, other):
        CountedNumber.checks += 1
        return self.value > other.value

    def __eq__(self, other):
        CountedNumber.checks += 1
        return self.value == other.value

    def __ne__(self, other):
        CountedNumber.checks += 1
        return self.value != other.value

    def __hash__(self):
        CountedNumber.checks += 1
        return hash(self.value)


# Отдельный подсчёт проверок для bytearray
def counted_bytearray(numbers):
    if not numbers:
        return 0, 0

    data = [CountedNumber(x) for x in numbers]
    CountedNumber.checks = 0

    low = min(data).value
    high = max(data).value

    checks = CountedNumber.checks

    seen = bytearray(high - low + 1)
    count = 0

    for x in numbers:
        index = x - low

        checks += 1

        if seen[index] == 0:
            seen[index] = 1
            count += 1

    return checks, count


def checks_worker(solution, numbers, queue):
    if solution == distinct_bytearray:
        checks, result = counted_bytearray(numbers)
    else:
        data = [CountedNumber(x) for x in numbers]

        CountedNumber.checks = 0

        result = solution(data)
        checks = CountedNumber.checks

    queue.put((checks, result))


def measure_checks(solution, numbers):
    queue = mp.Queue()

    process = mp.Process(
        target=checks_worker,
        args=(solution, numbers, queue)
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

    assert result == len(set(numbers))

    return checks


# 4. Подготовка данных и запуск замеров

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

    # 100 000 чисел от 0 до 99
    limited = [
        random.randint(0, 99)
        for _ in range(100000)
    ]

    print("Малый набор:", len(small))
    print("Большой набор:", len(large))
    print("Ограниченный диапазон:", len(limited))

    print("\nКоличество разных чисел:")
    print("Малый набор:", len(set(small)))
    print("Большой набор:", len(set(large)))
    print("Ограниченный диапазон:", len(set(limited)))

    # Замеры времени
    print("\nРезультаты замеров времени (мс):\n")

    for solution in solutions:
        t1 = measure_time(solution, small)
        t2 = measure_time(solution, large)
        t3 = measure_time(solution, limited)

        print(
            f"{solution.__name__:22} | {t1} | {t2} | {t3}",
            flush=True
        )

    # Замеры памяти
    print("\nПиковая память (КБ):\n")

    for solution in solutions:
        m1 = measure_memory(solution, small)
        m2 = measure_memory(solution, large)
        m3 = measure_memory(solution, limited)

        print(
            f"{solution.__name__:22} | {m1} | {m2} | {m3}",
            flush=True
        )

    # Подсчёт проверок
    print("\nКоличество проверок:\n")

    for solution in solutions:
        c1 = measure_checks(solution, small)
        c2 = measure_checks(solution, large)
        c3 = measure_checks(solution, limited)

        print(
            f"{solution.__name__:22} | {c1} | {c2} | {c3}",
            flush=True
        )
