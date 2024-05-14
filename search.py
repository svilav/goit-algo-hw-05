def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] == target:
            return (iterations, arr[mid])
        elif arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1

    if upper_bound is None and left < len(arr):
        upper_bound = arr[left]

    return (iterations, upper_bound)


sorted_array = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7]
target_value = 4.0
result = binary_search(sorted_array, target_value)
print(result)
