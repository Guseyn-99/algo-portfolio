
import heapq
from functools import reduce


# 1. Встроенная функция min()
def minimum_builtin(numbers):
    return min(numbers)


# 2. Линейный поиск через for
def minimum_for(numbers):
    result = numbers[0]

    for i in range(1, len(numbers)):
        if numbers[i] < result:
            result = numbers[i]

    return result


# 3. Линейный поиск через while
def minimum_while(numbers):
    result = numbers[0]
    i = 1

    while i < len(numbers):
        if numbers[i] < result:
            result = numbers[i]
        i += 1

    return result


# 4. Сортировка с созданием копии
def minimum_sorted(numbers):
    return sorted(numbers)[0]


# 5. Сортировка исходного списка
def minimum_sort(numbers):
    numbers.sort()
    return numbers[0]


# 6. Минимальная куча
def minimum_heap(numbers):
    heapq.heapify(numbers)
    return numbers[0]


# 7. Разделяй и властвуй
def minimum_recursive(numbers):
    def search(left, right):
        if left == right:
            return numbers[left]

        middle = (left + right) // 2

        left_min = search(left, middle)
        right_min = search(middle + 1, right)

        return min(left_min, right_min)

    return search(0, len(numbers) - 1)


# 8. Функциональный подход
def minimum_reduce(numbers):
    return reduce(min, numbers)


# Проверка всех решений
if __name__ == "__main__":
    numbers = [8, 3, 11, -2, 5]

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

    for i, solution in enumerate(solutions, 1):
        result = solution(numbers.copy())
        assert result == -2
        print(f"{i}. {solution.__name__}: {result}")
