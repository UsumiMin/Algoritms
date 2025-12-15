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

Используем оптимизированное построение суффиксного массива с подсчетом сортировки (counting sort) для маленького алфавита и LCP (Longest Common Prefix) массив.
"""

def counting_sort_for_radix(arr, exp, max_val):
    """Counting sort for radix sort implementation"""
    n = len(arr)
    output = [0] * n
    count = [0] * (max_val + 1)
    
    # Count occurrences
    for i in range(n):
        index = (arr[i] // exp) % max_val
        count[index] += 1
    
    # Change count[i] so that count[i] now contains actual position
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    # Build output array
    i = n - 1
    while i >= 0:
        index = (arr[i] // exp) % max_val
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1
    
    # Copy output array to arr
    for i in range(n):
        arr[i] = output[i]

def get_char_code(c):
    """Get character code for our alphabet"""
    return ord(c) - ord('a')

def build_suffix_array(s):
    """Build suffix array using a more efficient approach"""
    n = len(s)
    if n == 0:
        return []
    
    # Create suffixes with their original indices
    suffixes = []
    for i in range(n):
        suffixes.append((s[i:], i))
    
    # Sort using a custom comparison function with optimized approach
    # Instead of comparing full strings each time, we'll use a bucket sort approach
    # First, sort by first character, then refine...
    
    # Since we can't use complex data structures, let's optimize the existing approach
    # by implementing merge sort instead of insertion sort
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
            elif s1[0][i] > s2[0][i]:
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
    return sorted_suffixes

def solve(s):
    n = len(s)
    if n == 0:
        return 0
    
    # Build suffix array
    suffixes = build_suffix_array(s)
    
    # Total number of substrings without considering duplicates
    total = 0
    for i in range(n):
        total += (n - i)
    
    # Calculate LCP for adjacent suffixes in sorted order
    for i in range(1, n):
        suffix1 = suffixes[i][0]
        suffix2 = suffixes[i-1][0]
        
        # Find length of longest common prefix
        lcp = 0
        min_len = min(len(suffix1), len(suffix2))
        while lcp < min_len and suffix1[lcp] == suffix2[lcp]:
            lcp += 1
        
        # Subtract duplicate substrings count
        total -= lcp
    
    return total

def solve_optimized(s):
    """Optimized version using integer-based suffix array construction"""
    n = len(s)
    if n == 0:
        return 0
    
    # Convert string to numeric representation
    s_nums = [ord(c) - ord('a') for c in s]
    
    # Use counting sort based approach for suffix array
    # This is a simplified version of SA-IS or DC3 algorithm adapted to basic operations
    sa = list(range(n))  # Initialize suffix array with indices
    
    # Sort by first character using counting sort
    max_char = max(s_nums) if s_nums else 0
    count = [0] * (max_char + 2)
    
    for i in range(n):
        count[s_nums[i] + 1] += 1
    
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    temp_sa = [0] * n
    for i in range(n):
        temp_sa[count[s_nums[i]]] = sa[i]
        count[s_nums[i]] += 1
    
    sa = temp_sa[:]
    
    # Continue sorting with increasing length using a bucket sort approach
    # We'll implement a doubling approach similar to SA-IS but simplified
    rank = [0] * n
    tmp_rank = [0] * n
    
    # Initialize ranks based on first character
    for i in range(n):
        rank[i] = s_nums[i]
    
    length = 1
    while length < n:
        # Create tuples (rank[i], rank[i+length]) for sorting
        tuples = []
        for i in range(n):
            first = rank[i]
            second = rank[i + length] if i + length < n else -1
            tuples.append(((first, second), i))
        
        # Sort tuples using counting sort on pairs
        # First sort by second element (with negative values treated specially)
        # Then sort by first element
        # For simplicity, using a hybrid approach with optimized comparisons
        
        # Let's implement a more efficient approach
        # Group suffixes by their current rank pairs
        sorted_tuples = sorted(tuples)
        
        # Update ranks
        new_rank = 0
        for i in range(n):
            if i > 0 and sorted_tuples[i][0] != sorted_tuples[i-1][0]:
                new_rank += 1
            tmp_rank[sorted_tuples[i][1]] = new_rank
        
        rank[:] = tmp_rank[:]
        
        # If all ranks are unique, we're done
        if new_rank == n - 1:
            break
            
        length *= 2
    
    # Reconstruct suffix array from final ranks
    sa_with_ranks = [(rank[i], i) for i in range(n)]
    sa_with_ranks.sort()
    sa = [item[1] for item in sa_with_ranks]
    
    # Calculate total unique substrings
    total = n * (n + 1) // 2  # Total possible substrings
    
    # Calculate LCP array using Kasai's algorithm adapted
    rank_pos = [0] * n
    for i in range(n):
        rank_pos[sa[i]] = i
    
    lcp = [0] * n
    h = 0
    for i in range(n):
        if rank_pos[i] > 0:
            j = sa[rank_pos[i] - 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rank_pos[i]] = h
            if h > 0:
                h -= 1
    
    # Subtract duplicate substrings
    for i in range(1, n):
        total -= lcp[i]
    
    return total

def test1():
    s = "aaba"
    result = solve_optimized(s)
    assert result == 8

def test2():
    s = "aaaa"
    result = solve_optimized(s)
    assert result == 4

def test3():
    s = "abc"
    result = solve_optimized(s)
    assert result == 6

def test4():
    s = "a"
    result = solve_optimized(s)
    assert result == 1

def test5():
    s = "abab"
    result = solve_optimized(s)
    assert result == 7

def test6():
    s = "abcd"
    result = solve_optimized(s)
    assert result == 10

def test7():
    s = "a" * 5000
    result = solve_optimized(s)
    assert result == 5000

def test8():
    s = "abcdefghij"
    result = solve_optimized(s)
    expected = 10 * 11 // 2
    assert result == expected

def test9():
    s = "ababab"
    result = solve_optimized(s)
    assert result > 0

def test10():
    s = "aaaaa"
    result = solve_optimized(s)
    assert result == 5

def main():
    test1()
    s = input().strip()
    start_time = time.time()
    result = solve_optimized(s)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()
    
    print(result)
    print(f"Время: {end_time - start_time:.3f} сек")
    print(f"Память: {peak / 1024:.1f} KB")

if __name__ == "__main__":
    main()