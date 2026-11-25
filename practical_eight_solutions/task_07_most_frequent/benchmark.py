
import random
import time
import tracemalloc
import statistics
import multiprocessing as mp

from solutions import (
    frequent_dict,
    frequent_counter,
    frequent_online,
    frequent_sorted,
    frequent_sort,
    frequent_array,
    frequent_count,
    frequent_set_count,
)


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


# Подсчёт сравнений и вычислений хешей
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

    def __sub__(self, other):
        return self.value - other.value

    def __add__(self, other):
        return self.value + other


# Выполнение отдельного замера
def worker(solution, numbers, mode, queue):
    data = numbers.copy()

    if mode == "time":
        start = time.perf_counter()
        result = solution(data)
        value = (time.perf_counter() - start) * 1000

    elif mode == "memory":
        tracemalloc.start()
        result = solution(data)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        value = peak / 1024

    else:
        data = [CountedNumber(x) for x in data]
        CountedNumber.checks = 0

        result = solution(data)
        value = CountedNumber.checks

        if isinstance(result, CountedNumber):
            result = result.value

    queue.put((value, result))


def run_measurement(solution, numbers, mode):
    queue = mp.Queue()

    process = mp.Process(
        target=worker,
        args=(solution, numbers, mode, queue)
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
        raise RuntimeError("Ошибка выполнения замера")

    value, result = queue.get(timeout=1)
    queue.close()

    assert result == frequent_dict(numbers)

    return value


def measure(solution, numbers, mode):
    repeats = 5 if mode == "time" else 1
    values = []

    for _ in range(repeats):
        value = run_measurement(solution, numbers, mode)

        if value == "TIMEOUT":
            return "TIMEOUT"

        values.append(value)

    if mode == "checks":
        return values[0]

    return f"{statistics.median(values):.4f}"


# Подготовка данных
if __name__ == "__main__":
    random.seed(42)

    small = [
        random.randint(0, 1000000)
        for _ in range(1000)
    ]

    large = [
        random.randint(0, 1000000)
        for _ in range(100000)
    ]

    limited = [
        random.randint(0, 100)
        for _ in range(100000)
    ]

    datasets = [small, large, limited]

    print("Малый набор:", len(small))
    print("Большой набор:", len(large))
    print("Ограниченный диапазон:", len(limited))

    print("\nСамые частые числа:")

    for numbers in datasets:
        result = frequent_dict(numbers)

        print(
            f"Число: {result}, "
            f"частота: {numbers.count(result)}"
        )

    modes = [
        ("time", "Результаты замеров времени (мс)"),
        ("memory", "Пиковая память (КБ)"),
        ("checks", "Количество проверок"),
    ]

    for mode, title in modes:
        print(f"\n{title}:\n")

        for solution in solutions:
            values = [
                measure(solution, numbers, mode)
                for numbers in datasets
            ]

            print(
                f"{solution.__name__:22} | "
                + " | ".join(map(str, values)),
                flush=True
            )
