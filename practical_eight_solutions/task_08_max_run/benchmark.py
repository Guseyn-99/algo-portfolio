
import random
import time
import tracemalloc
import statistics
import multiprocessing as mp

from solutions import (
    max_run_index,
    max_run_iterator,
    max_run_pointers,
    max_run_groupby,
    max_run_dp,
    max_run_zip,
    max_run_nested,
    max_run_divide,
)


solutions = [
    max_run_index,
    max_run_iterator,
    max_run_pointers,
    max_run_groupby,
    max_run_dp,
    max_run_zip,
    max_run_nested,
    max_run_divide,
]


# Подсчёт сравнений элементов
class CountedNumber:
    checks = 0

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        CountedNumber.checks += 1
        return self.value == other.value

    def __ne__(self, other):
        CountedNumber.checks += 1
        return self.value != other.value


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

    assert result == max_run_index(numbers)

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
        random.randint(0, 100)
        for _ in range(1000)
    ]

    large = [
        random.randint(0, 100)
        for _ in range(100000)
    ]

    # Серия из 10 000 одинаковых чисел в конце
    end_run = [
        random.randint(0, 100)
        for _ in range(90000)
    ] + [101] * 10000

    datasets = [small, large, end_run]

    print("Малый набор:", len(small))
    print("Большой набор:", len(large))
    print("Серия в конце:", len(end_run))

    print("\nМаксимальные серии:")

    for numbers in datasets:
        print(max_run_index(numbers))

    modes = [
        ("time", "Результаты замеров времени (мс)"),
        ("memory", "Пиковая память (КБ)"),
        ("checks", "Количество сравнений элементов"),
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
