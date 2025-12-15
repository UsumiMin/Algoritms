import time
import tracemalloc

tracemalloc.start()

"""
### Условие

Ограничение времени: 2.0 секунды
Ограничение памяти: 64 МБ
Программисту Васе не повезло — вместо отпуска его послали в командировку, на научную конференцию. 
Надо повышать уровень знаний, сказал начальник, важная конференция по криптографии, 
проводится во Франции — а там шифровали еще во времена Ришелье и взламывали чужие шифры еще во времена Виета.
Вася быстро выяснил, что все луврские картины он уже где-то видел, вид эйфелевой башни приелся ему еще раньше, 
чем мышка стерла его с коврика, а такие стеклянные пирамиды у нас делают надо всякими киосками и сомнительными забегаловками. 
Одним словом, смотреть в Париже оказалось просто не на что, рыбу половить негде, поэтому Васе пришлось посещать доклады на конференции.
Один из докладчиков, в очередной раз пытаясь разгадать шифры Бэкона, выдвинул гипотезу, что ключ к тайнам Бэкона можно подобрать, 
проанализировав все возможные подстроки произведений Бэкона.
«Но их же слишком много!» — вслух удивился Вася.
«Нет, не так уж и много!» — закричал докладчик — «подсчитайте и вы сами убедитесь!».
Тем же вечером Вася нашел в интернете полное собрание сочинений Бэкона. 
Он написал программу, которая переработала тексты в одну длинную строку, выкинув из текстов все пробелы и знаки препинания. 
И вот теперь Вася весьма озадачен — а как же подсчитать количество различных подстрок этой строки?

### Ход решения

Используем суффиксный массив с ручной сортировкой и LCP (Longest Common Prefix) массив.
Количество различных подстрок = общее количество подстрок - количество повторяющихся.
Можно вычислить как: сумма (n-i) для i от 0 до n-1 минус сумма всех LCP между соседними суффиксами в отсортированном порядке.

"""
    
def solve(s):
    """Count unique substrings using suffix array and LCP with O(n log n) complexity"""
    n = len(s)
    if n == 0:
        return 0

    # For small strings, use a direct approach to avoid algorithm overhead
    if n <= 100:
        substrings = set()
        for i in range(n):
            for j in range(i + 1, n + 1):
                substrings.add(s[i:j])
        return len(substrings)

    # Convert string to numbers for efficient processing
    s_nums = [ord(c) for c in s]

    # Build suffix array using the doubling algorithm
    sa = [0] * n
    rank = [0] * n
    tmp = [0] * n
    tmp2 = [[0, 0, 0] for _ in range(n)]  # [first_rank, second_rank, original_index]

    # Initial ranking by first character using counting sort
    max_char = max(s_nums) if s_nums else 0
    cnt = [0] * (max_char + 1)

    for i in range(n):
        cnt[s_nums[i]] += 1

    for i in range(1, len(cnt)):
        cnt[i] += cnt[i - 1]

    # Build initial suffix array by sorting on first character (stable sort)
    for i in range(n-1, -1, -1):
        cnt[s_nums[i]] -= 1
        sa[cnt[s_nums[i]]] = i

    # Assign initial ranks
    r = 0
    rank[sa[0]] = 0
    for i in range(1, n):
        if s_nums[sa[i]] != s_nums[sa[i-1]]:
            r += 1
        rank[sa[i]] = r

    # Doubling algorithm - O(log n) iterations, each O(n)
    k = 1
    while k < n and r < n - 1:
        # Create pairs [rank[i], rank[i+k], i] and sort by these pairs
        for i in range(n):
            tmp2[i][0] = rank[i]  # first element of pair
            tmp2[i][1] = rank[i + k] if i + k < n else -1  # second element of pair
            tmp2[i][2] = i  # original index

        # Radix sort: first by second element, then by first element

        # Sort by second element (stable sort)
        counting_max = r + 2  # +2 to handle -1 case (shift by +1 to make it non-negative)
        cnt = [0] * counting_max

        for i in range(n):
            sec = tmp2[i][1]
            cnt[sec + 1 if sec >= 0 else 0] += 1  # -1 -> 0, 0 -> 1, 1 -> 2, etc.

        for i in range(1, len(cnt)):
            cnt[i] += cnt[i - 1]

        new_sa = [0] * n
        for i in range(n-1, -1, -1):  # Stable sort
            sec = tmp2[i][1]
            pos = cnt[sec + 1 if sec >= 0 else 0]
            cnt[sec + 1 if sec >= 0 else 0] -= 1
            new_sa[pos - 1] = tmp2[i][2]  # original index

        # Now sort by first element (stable sort)
        cnt = [0] * (r + 1)
        for i in range(n):
            first = rank[new_sa[i]]
            cnt[first] += 1

        for i in range(1, len(cnt)):
            cnt[i] += cnt[i - 1]

        for i in range(n-1, -1, -1):  # Stable sort
            first = rank[new_sa[i]]
            pos = cnt[first]
            cnt[first] -= 1
            sa[pos - 1] = new_sa[i]

        # Update ranks based on pairs
        tmp[sa[0]] = r = 0
        for i in range(1, n):
            # Compare pairs (rank[sa[i-1]], rank[sa[i-1]+k]) and (rank[sa[i]], rank[sa[i]+k])
            prev_pair = (rank[sa[i-1]], rank[sa[i-1] + k] if sa[i-1] + k < n else -1)
            curr_pair = (rank[sa[i]], rank[sa[i] + k] if sa[i] + k < n else -1)

            if prev_pair != curr_pair:
                r += 1
            tmp[sa[i]] = r

        rank, tmp = tmp, rank
        k *= 2

    # Calculate LCP array using Kasai's algorithm
    lcp = [0] * n
    rank_pos = [0] * n  # rank_pos[i] = position of suffix s[i:] in sorted suffix array
    for i in range(n):
        rank_pos[sa[i]] = i

    h = 0
    for i in range(n):
        if rank_pos[i] > 0:
            j = sa[rank_pos[i] - 1]  # previous suffix in sorted order
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rank_pos[i]] = h
            if h > 0:
                h -= 1

    # Total unique substrings = total possible - sum of LCP values
    total = n * (n + 1) // 2
    for i in range(1, n):
        total -= lcp[i]

    return total

def test1():
    s = "aaba"
    result = solve(s)
    assert result == 8

def test2():
    s = "aaaa"
    result = solve(s)
    assert result == 4

def test3():
    s = "abc"
    result = solve(s)
    assert result == 6

def test4():
    s = "a"
    result = solve(s)
    assert result == 1

def test5():
    s = "abab"
    result = solve(s)
    assert result == 7

def test6():
    s = "abcd"
    result = solve(s)
    assert result == 10

def test7():
    s = "a" * 5000
    result = solve(s)
    assert result == 5000

def test8():
    s = "abcdefghij"
    result = solve(s)
    expected = 10 * 11 // 2
    assert result == expected

def test9():
    s = "ababab"
    result = solve(s)
    assert result > 0

def test10():
    s = "aaaaa"
    result = solve(s)
    assert result == 5

def main():
    test1()
    s = input().strip()
    start_time = time.time()
    result = solve(s)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()
    
    print(result)
    print(f"Время: {end_time - start_time:.3f} сек")
    print(f"Память: {peak / 1024:.1f} KB")

if __name__ == "__main__":
    main()