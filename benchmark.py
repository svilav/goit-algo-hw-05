import timeit


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def knuth_morris_pratt(text, pattern):
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp(text, pattern):
    substring_length = len(pattern)
    main_string_length = len(text)

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(pattern, base, modulus)
    current_slice_hash = polynomial_hash(text[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if text[i:i + substring_length] == pattern:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(text[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(text[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def measure_time(algorithm, text, pattern):
    return timeit.timeit(lambda: algorithm(text, pattern), number=1000)


with open('1.txt', 'r', encoding='utf-8') as file:
    text1 = file.read()

with open('2.txt', 'r', encoding='utf-8') as file:
    text2 = file.read()



existing_substring = "приклад"
non_existing_substring = "вигаданийпідрядок"

# Вимірювання для статті 1
time_bm_existing_1 = measure_time(boyer_moore, text1, existing_substring)
time_kmp_existing_1 = measure_time(knuth_morris_pratt, text1, existing_substring)
time_rk_existing_1 = measure_time(rabin_karp, text1, existing_substring)

time_bm_non_existing_1 = measure_time(boyer_moore, text1, non_existing_substring)
time_kmp_non_existing_1 = measure_time(knuth_morris_pratt, text1, non_existing_substring)
time_rk_non_existing_1 = measure_time(rabin_karp, text1, non_existing_substring)


time_bm_existing_2 = measure_time(boyer_moore, text2, existing_substring)
time_kmp_existing_2 = measure_time(knuth_morris_pratt, text2, existing_substring)
time_rk_existing_2 = measure_time(rabin_karp, text2, existing_substring)

time_bm_non_existing_2 = measure_time(boyer_moore, text2, non_existing_substring)
time_kmp_non_existing_2 = measure_time(knuth_morris_pratt, text2, non_existing_substring)
time_rk_non_existing_2 = measure_time(rabin_karp, text2, non_existing_substring)


results = {
    "стаття 1": {
        "існуючий підрядок": {
            "Боєр-Мур": time_bm_existing_1,
            "Кнут-Морріс-Пратт": time_kmp_existing_1,
            "Рабін-Карп": time_rk_existing_1
        },
        "вигаданий підрядок": {
            "Боєр-Мур": time_bm_non_existing_1,
            "Кнут-Морріс-Пратт": time_kmp_non_existing_1,
            "Рабін-Карп": time_rk_non_existing_1
        }
    },
    "стаття 2": {
        "існуючий підрядок": {
            "Боєр-Мур": time_bm_existing_2,
            "Кнут-Морріс-Пратт": time_kmp_existing_2,
            "Рабін-Карп": time_rk_existing_2
        },
        "вигаданий підрядок": {
            "Боєр-Мур": time_bm_non_existing_2,
            "Кнут-Морріс-Пратт": time_kmp_non_existing_2,
            "Рабін-Карп": time_rk_non_existing_2
        }
    }
}


for article, data in results.items():
    for substring_type, times in data.items():
        fastest_algorithm = min(times, key=times.get)
        print(
            f"Для {article} і {substring_type} найшвидший алгоритм: {fastest_algorithm} з часом {times[fastest_algorithm]:.6f} секунд")


total_times = {
    "Боєр-Мур": sum(
        [results[article][substring_type]["Боєр-Мур"] for article in results for substring_type in results[article]]),
    "Кнут-Морріс-Пратт": sum(
        [results[article][substring_type]["Кнут-Морріс-Пратт"] for article in results for substring_type in
         results[article]]),
    "Рабін-Карп": sum(
        [results[article][substring_type]["Рабін-Карп"] for article in results for substring_type in results[article]])
}

fastest_algorithm_overall = min(total_times, key=total_times.get)
print(
    f"Найшвидший алгоритм в цілому: {fastest_algorithm_overall} з загальним часом {total_times[fastest_algorithm_overall]:.6f} секунд")