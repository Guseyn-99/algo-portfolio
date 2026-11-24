import random
import time
import tracemalloc
import statistics

from solutions import (
    minimum_builtin,
    minimum_for,
    minimum_while,
    minimum_sorted,
    minimum_sort,
    minimum_heap,
    minimum_recursive,
    minimum_reduce,
)

# Фиксируем генерацию случайных чисел
random.seed(42)

# Наборы данных для эксперимента
small = [random.randint(-1000000, 1000000) for _ in range(1000)]
large = [random.randint(-1000000, 1000000) for _ in range(100000)]

# Набор данных с минимумом в конце
minimum_at_end = [
    random.randint(0, 1000000) for _ in range(99999)
]
minimum_at_end.append(-1)

print("Малый набор:", len(small))
print("Большой набор:", len(large))
print("Минимум в конце:", len(minimum_at_end))

solutions = [
    minimum_builtin,
    minimum_for,
    minimum_while,
    minimum_sorted,
    minimum_sort,
    minimum_heap,
    minimum_recursive,
    minimum_reduce,
]


def measure_time(solution, numbers):
    times = []

    for _ in range(5):
        data = numbers.copy()

        start = time.perf_counter()
        result = solution(data)
        end = time.perf_counter()

        times.append((end - start) * 1000)

        assert result == min(numbers)

    return statistics.median(times)


print("\nРезультаты замеров времени (мс):\n")

for solution in solutions:
    t1 = measure_time(solution, small)
    t2 = measure_time(solution, large)
    t3 = measure_time(solution, minimum_at_end)

    print(f"{solution.__name__:20} | {t1:.4f} | {t2:.4f} | {t3:.4f}")

    
def measure_memory(solution, numbers):
    data = numbers.copy()

    tracemalloc.start()
    result = solution(data)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    assert result == min(numbers)

    return peak / 1024


print("\nПиковая память (КБ):\n")

for solution in solutions:
    m1 = measure_memory(solution, small)
    m2 = measure_memory(solution, large)
    m3 = measure_memory(solution, minimum_at_end)

    print(f"{solution.__name__:20} | {m1:.4f} | {m2:.4f} | {m3:.4f}")


class CountedNumber:
    comparisons = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        CountedNumber.comparisons += 1
        return self.value < other.value


def measure_comparisons(solution, numbers):
    data = [CountedNumber(x) for x in numbers]

    CountedNumber.comparisons = 0

    result = solution(data)

    assert result.value == min(numbers)

    return CountedNumber.comparisons


print("\nКоличество сравнений:\n")

for solution in solutions:
    c1 = measure_comparisons(solution, small)
    c2 = measure_comparisons(solution, large)
    c3 = measure_comparisons(solution, minimum_at_end)

    print(f"{solution.__name__:20} | {c1} | {c2} | {c3}")
