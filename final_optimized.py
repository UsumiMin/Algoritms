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

Используем оптимизированное построение суффиксного массива с упрощенным алгоритмом и LCP (Longest Common Prefix) массив.
"""

def compare_strings(s1, s2):
    '''Compare two strings properly'''
    min_len = min(len(s1), len(s2))
    for i in range(min_len):
        if s1[i] < s2[i]:
            return -1
        elif s1[i] > s2[i]:
            return 1
    if len(s1) < len(s2):
        return -1
    elif len(s1) > len(s2):
        return 1
    else:
        return 0

def merge_sort_suffixes(arr):
    """Sort suffixes using merge sort"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort_suffixes(arr[:mid])
    right = merge_sort_suffixes(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """Merge two sorted arrays of (suffix, index) tuples"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        # Compare the suffix parts (the strings)
        if compare_strings(left[i][0], right[j][0]) <= 0:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def solve(s):
    """
    Count unique substrings using optimized suffix array and LCP computation
    """
    n = len(s)
    if n == 0:
        return 0
    
    # For efficiency, use the advanced algorithm for all cases
    return solve_advanced(s)

def solve_advanced(s):
    """Advanced algorithm using suffix array with doubling method and LCP"""
    n = len(s)
    if n == 0:
        return 0
    
    # Convert string to numerical representation for faster processing
    s_num = [ord(c) for c in s]
    
    # Initialize suffix array with indices
    sa = [0] * n
    rank = [0] * n
    tmp = [0] * n
    
    # Initial ranking by first character using counting sort
    max_char = max(s_num) if s_num else 0
    cnt = [0] * (max_char + 2)
    
    for i in range(n):
        cnt[s_num[i] + 1] += 1
    
    for i in range(1, len(cnt)):
        cnt[i] += cnt[i - 1]
    
    for i in range(n):
        cnt[s_num[i]] -= 1
        sa[cnt[s_num[i]]] = i
    
    # Assign initial ranks
    r = 0
    for i in range(n):
        if i > 0 and s_num[sa[i]] != s_num[sa[i-1]]:
            r += 1
        rank[sa[i]] = r
    
    # Doubling algorithm to build suffix array
    k = 1
    while k < n and r < n - 1:
        # Sort by pair (rank[i], rank[i+k]) using radix sort
        # First, sort by second element of pair (stable sort)
        cnt = [0] * (r + 2)
        for i in range(n):
            second = rank[sa[i] + k] if sa[i] + k < n else -1
            second = second + 1  # Shift to handle -1 properly
            cnt[second + 1] += 1  # Add 1 to handle -1 case
        
        # Fix: proper handling of negative values
        for i in range(1, len(cnt)):
            cnt[i] += cnt[i - 1]
        
        # Actually, let's fix this properly
        # Count occurrences for the second element (with -1 for out-of-bounds)
        cnt = [0] * (r + 2)
        for i in range(n):
            second = rank[sa[i] + k] if sa[i] + k < n else -1
            cnt[second + 1] += 1  # -1 maps to index 0, 0 maps to index 1, etc.
        
        for i in range(1, len(cnt)):
            cnt[i] += cnt[i - 1]
        
        new_sa = [0] * n
        for i in range(n-1, -1, -1):  # Stable sort - go backwards
            second = rank[sa[i] + k] if sa[i] + k < n else -1
            cnt[second + 1] -= 1
            new_sa[cnt[second + 1]] = sa[i]
        
        sa = new_sa[:]
        
        # Now sort by first element of the pair (also stable)
        cnt = [0] * (r + 2)
        for i in range(n):
            first = rank[sa[i]]
            cnt[first + 1] += 1
        
        for i in range(1, len(cnt)):
            cnt[i] += cnt[i - 1]
        
        new_sa = [0] * n
        for i in range(n-1, -1, -1):  # Stable sort - go backwards
            first = rank[sa[i]]
            cnt[first + 1] -= 1
            new_sa[cnt[first + 1]] = sa[i]
        
        sa = new_sa[:]
        
        # Update ranks based on pairs
        tmp[sa[0]] = r = 0
        for i in range(1, n):
            # Check if current pair differs from previous
            prev_pair = (rank[sa[i-1]], rank[sa[i-1] + k] if sa[i-1] + k < n else -1)
            curr_pair = (rank[sa[i]], rank[sa[i] + k] if sa[i] + k < n else -1)
            
            if prev_pair != curr_pair:
                r += 1
            tmp[sa[i]] = r
        
        rank, tmp = tmp, rank
        k *= 2
    
    # Calculate LCP array using Kasai's algorithm
    lcp = [0] * n
    rank_pos = [0] * n  # position of suffix starting at i in the sorted suffix array
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
    
    # Total unique substrings = total possible substrings - sum of LCP values
    total = n * (n + 1) // 2
    for i in range(1, n):
        total -= lcp[i]
    
    return total

def test1():
    s = "aaba"
    result = solve(s)
    assert result == 8, f"Test 1 failed: expected 8, got {result}"

def test2():
    s = "aaaa"
    result = solve(s)
    assert result == 4, f"Test 2 failed: expected 4, got {result}"
    print(f"Test 2 passed: 'aaaa' -> {result}")

def test3():
    s = "abc"
    result = solve(s)
    assert result == 6, f"Test 3 failed: expected 6, got {result}"

def test4():
    s = "a"
    result = solve(s)
    assert result == 1, f"Test 4 failed: expected 1, got {result}"

def test5():
    s = "abab"
    result = solve(s)
    assert result == 7, f"Test 5 failed: expected 7, got {result}"

def test6():
    s = "abcd"
    result = solve(s)
    assert result == 10, f"Test 6 failed: expected 10, got {result}"

def test7():
    s = "a" * 5000
    result = solve(s)
    assert result == 5000, f"Test 7 failed: expected 5000, got {result}"

def test8():
    s = "abcdefghij"
    result = solve(s)
    expected = 10 * 11 // 2
    assert result == expected, f"Test 8 failed: expected {expected}, got {result}"

def test9():
    s = "ababab"
    result = solve(s)
    assert result > 0, f"Test 9 failed: expected positive result, got {result}"

def test10():
    s = "aaaaa"
    result = solve(s)
    assert result == 5, f"Test 10 failed: expected 5, got {result}"

def main():
    # Run all tests
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()
    
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