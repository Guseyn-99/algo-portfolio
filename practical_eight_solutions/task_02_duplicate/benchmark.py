
import random
import time
import tracemalloc
import statistics
import multiprocessing as mp

from solutions import (
    duplicate_set,
    duplicate_set_loop,
    duplicate_dict,
    duplicate_counter,
    duplicate_sorted,
    duplicate_sort,
    duplicate_nested,
    duplicate_bisect,
)


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


def time_worker(solution, numbers, queue):
    data = numbers.copy()

    start = time.perf_counter()
    result = solution(data)
    end = time.perf_counter()

    queue.put((end - start, result))


def measure_time(solution, numbers):
    times = []
    expected = len(numbers) != len(set(numbers))

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

        elapsed, result = queue.get(timeout=1)
        queue.close()

        assert result == expected

        if elapsed > 2:
            return "TIMEOUT"

        times.append(elapsed * 1000)

    return f"{statistics.median(times):.4f}"


if __name__ == "__main__":
    random.seed(42)

    small = [random.randint(0, 10000) for _ in range(1000)]

    large = list(range(100000))
    random.shuffle(large)

    duplicate_at_end = list(range(99999))
    random.shuffle(duplicate_at_end)
    duplicate_at_end.append(duplicate_at_end[-1])

    print("Малый набор:", len(small))
    print("Большой набор:", len(large))
    print("Повтор в конце:", len(duplicate_at_end))

    print("\nРезультаты замеров времени (мс):\n")

    for solution in solutions:
        t1 = measure_time(solution, small)
        t2 = measure_time(solution, large)
        t3 = measure_time(solution, duplicate_at_end)

        print(f"{solution.__name__:22} | {t1} | {t2} | {t3}", flush=True)


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

    peak, result = queue.get(timeout=1)
    queue.close()

    assert result == (len(numbers) != len(set(numbers)))

    return f"{peak:.4f}"


if __name__ == "__main__":
    print("\nПиковая память (КБ):\n")

    for solution in solutions:
        m1 = measure_memory(solution, small)
        m2 = measure_memory(solution, large)
        m3 = measure_memory(solution, duplicate_at_end)

        print(f"{solution.__name__:22} | {m1} | {m2} | {m3}", flush=True)



class CountedNumber:
    comparisons = 0
    hashes = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        CountedNumber.comparisons += 1
        return self.value < other.value

    def __eq__(self, other):
        CountedNumber.comparisons += 1
        return self.value == other.value

    def __hash__(self):
        CountedNumber.hashes += 1
        return hash(self.value)


def checks_worker(solution, numbers, queue):
    data = [CountedNumber(x) for x in numbers]

    CountedNumber.comparisons = 0
    CountedNumber.hashes = 0

    result = solution(data)

    checks = (
        CountedNumber.comparisons
        + CountedNumber.hashes
    )

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

    checks, result = queue.get(timeout=1)
    queue.close()

    assert result == (len(numbers) != len(set(numbers)))

    return checks


if __name__ == "__main__":
    print("\nКоличество проверок:\n")

    for solution in solutions:
        c1 = measure_checks(solution, small)
        c2 = measure_checks(solution, large)
        c3 = measure_checks(solution, duplicate_at_end)

        print(f"{solution.__name__:22} | {c1} | {c2} | {c3}", flush=True)
