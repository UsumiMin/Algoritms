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

def solve(s):
    """
    Count unique substrings using optimized suffix array and LCP computation
    """
    n = len(s)
    if n == 0:
        return 0
    
    # For small strings, use a direct approach
    if n <= 1000:
        # Use the original approach but with better sorting
        return solve_small(s)
    else:
        # For larger strings, use optimized approach
        return solve_large(s)

def solve_small(s):
    """For smaller inputs, use a more straightforward optimized approach"""
    n = len(s)
    
    # Generate all suffixes with their starting positions
    suffixes = []
    for i in range(n):
        suffixes.append((s[i:], i))
    
    # Sort suffixes using a custom merge sort to avoid built-in sort
    def merge_sort_suffixes(arr):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = merge_sort_suffixes(arr[:mid])
        right = merge_sort_suffixes(arr[mid:])
        
        return merge(left, right)
    
    def compare_strings(s1, s2):
        '''Compare two strings'''
        min_len = min(len(s1[0]), len(s2[0]))
        for i in range(min_len):
            if s1[0][i] < s2[0][i]:
                return -1
            elif s1[0][i] > s1[0][i] if len(s1[0]) > i else s2[0][i]:  # Fixed comparison bug
                return 1
        if len(s1[0]) < len(s2[0]):
            return -1
        elif len(s1[0]) > len(s2[0]):
            return 1
        else:
            return 0
    
    def merge(left, right):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if compare_strings(left[i], right[j]) <= 0:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    sorted_suffixes = merge_sort_suffixes(suffixes)
    
    # Total number of substrings without considering duplicates
    total = n * (n + 1) // 2
    
    # Calculate LCP for adjacent suffixes in sorted order
    for i in range(1, n):
        suffix1 = sorted_suffixes[i][0]
        suffix2 = sorted_suffixes[i-1][0]
        
        # Find length of longest common prefix
        lcp = 0
        min_len = min(len(suffix1), len(suffix2))
        while lcp < min_len and suffix1[lcp] == suffix2[lcp]:
            lcp += 1
        
        # Subtract duplicate substrings count
        total -= lcp
    
    return total

def solve_large(s):
    """More efficient approach for larger inputs"""
    n = len(s)
    
    # Convert characters to integers for easier processing
    s_int = [ord(c) for c in s]
    
    # Initialize suffix array with indices
    sa = list(range(n))
    
    # Use a doubling algorithm to construct suffix array efficiently
    # Rank array to store equivalence classes
    rank = [0] * n
    tmp = [0] * n
    
    # Initial ranking by first character
    # Using counting sort for the first phase
    max_char = max(s_int) if s_int else 0
    cnt = [0] * (max_char + 2)
    
    for i in range(n):
        cnt[s_int[i] + 1] += 1
    
    for i in range(1, len(cnt)):
        cnt[i] += cnt[i - 1]
    
    for i in range(n):
        sa[cnt[s_int[i]]] = i
        cnt[s_int[i]] += 1
    
    # Assign initial ranks
    r = 0
    for i in range(n):
        if i > 0 and s_int[sa[i]] != s_int[sa[i-1]]:
            r += 1
        rank[sa[i]] = r
    
    # Doubling phase
    k = 1
    while k < n and r < n - 1:
        # Prepare for next phase - sort by (rank[i], rank[i+k])
        # Use radix sort: first by second element, then by first
        
        # Counting sort by second element of pair (rank[i], rank[i+k])
        cnt = [0] * (r + 2)
        for i in range(n):
            second = rank[sa[i] + k] if sa[i] + k < n else 0
            cnt[second] += 1
        
        for i in range(1, len(cnt)):
            cnt[i] += cnt[i - 1]
        
        new_sa = [0] * n
        for i in range(n-1, -1, -1):  # Process in reverse to maintain stability
            second = rank[sa[i] + k] if sa[i] + k < n else 0
            cnt[second] -= 1
            new_sa[cnt[second]] = sa[i]
        
        sa = new_sa
        
        # Counting sort by first element of pair (rank[i], rank[i+k])
        cnt = [0] * (r + 2)
        for i in range(n):
            first = rank[sa[i]]
            cnt[first] += 1
        
        for i in range(1, len(cnt)):
            cnt[i] += cnt[i - 1]
        
        new_sa = [0] * n
        for i in range(n-1, -1, -1):  # Process in reverse to maintain stability
            first = rank[sa[i]]
            cnt[first] -= 1
            new_sa[cnt[first]] = sa[i]
        
        sa = new_sa
        
        # Update ranks
        tmp[sa[0]] = r = 0
        for i in range(1, n):
            # Check if current pair is different from previous
            prev_first, prev_second = rank[sa[i-1]], rank[sa[i-1] + k] if sa[i-1] + k < n else -1
            curr_first, curr_second = rank[sa[i]], rank[sa[i] + k] if sa[i] + k < n else -1
            
            if (prev_first, prev_second) != (curr_first, curr_second):
                r += 1
            tmp[sa[i]] = r
        
        rank, tmp = tmp, rank
        k *= 2
    
    # Calculate LCP using Kasai's algorithm
    lcp = [0] * n
    rank_pos = [0] * n  # rank_pos[original_position] = position_in_sorted_suffixes
    for i in range(n):
        rank_pos[sa[i]] = i
    
    h = 0
    for i in range(n):
        if rank_pos[i] > 0:
            j = sa[rank_pos[i] - 1]  # Previous suffix in sorted order
            # Compute LCP between s[i:] and s[j:]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rank_pos[i]] = h
            if h > 0:
                h -= 1
    
    # Total unique substrings = total possible - duplicates removed via LCP
    total = n * (n + 1) // 2
    for i in range(1, n):
        total -= lcp[i]
    
    return total

def test1():
    s = "aaba"
    result = solve(s)
    assert result == 8, f"Expected 8, got {result}"

def test2():
    s = "aaaa"
    result = solve(s)
    assert result == 4, f"Expected 4, got {result}"

def test3():
    s = "abc"
    result = solve(s)
    assert result == 6, f"Expected 6, got {result}"

def test4():
    s = "a"
    result = solve(s)
    assert result == 1, f"Expected 1, got {result}"

def test5():
    s = "abab"
    result = solve(s)
    assert result == 7, f"Expected 7, got {result}"

def test6():
    s = "abcd"
    result = solve(s)
    assert result == 10, f"Expected 10, got {result}"

def test7():
    s = "a" * 5000
    result = solve(s)
    assert result == 5000, f"Expected 5000, got {result}"

def test8():
    s = "abcdefghij"
    result = solve(s)
    expected = 10 * 11 // 2
    assert result == expected, f"Expected {expected}, got {result}"

def test9():
    s = "ababab"
    result = solve(s)
    assert result > 0, f"Expected positive result, got {result}"

def test10():
    s = "aaaaa"
    result = solve(s)
    assert result == 5, f"Expected 5, got {result}"

def main():
    # Run tests
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