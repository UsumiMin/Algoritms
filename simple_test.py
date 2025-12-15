def solve(s):
    """Count unique substrings using suffix array and LCP"""
    n = len(s)
    if n == 0:
        return 0
    
    # Special case for small strings to avoid complex algorithm overhead
    if n <= 100:
        # For small strings, use a direct approach
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
    tmp2 = [[0, 0, 0] for _ in range(n)]  # [first, second, new_rank]
    
    # Initial ranking by first character using counting sort
    max_char = max(s_nums) if s_nums else 0
    cnt = [0] * (max_char + 1)
    
    for i in range(n):
        cnt[s_nums[i]] += 1
    
    for i in range(1, len(cnt)):
        cnt[i] += cnt[i - 1]
    
    # Build initial suffix array by sorting on first character
    for i in range(n-1, -1, -1):  # Stable sort
        cnt[s_nums[i]] -= 1
        sa[cnt[s_nums[i]]] = i
    
    # Assign initial ranks
    r = 0
    rank[sa[0]] = 0
    for i in range(1, n):
        if s_nums[sa[i]] != s_nums[sa[i-1]]:
            r += 1
        rank[sa[i]] = r
    
    k = 1
    while k < n and r < n - 1:
        # Create pairs [rank[i], rank[i+k], i] and sort by these pairs
        for i in range(n):
            tmp2[i][0] = rank[i]
            tmp2[i][1] = rank[i + k] if i + k < n else -1
            tmp2[i][2] = i
        
        # Sort by second element first (stable sort)
        # Count occurrences of second elements
        counting_max = r + 2  # +2 to handle -1 case (shift by +1)
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
        
        # Now sort by first element
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

def test_case(s, expected):
    result = solve(s)
    print(f"Input: '{s}' -> Output: {result}, Expected: {expected}, {'✓' if result == expected else '✗'}")
    if result != expected:
        print(f"  FAIL: Got {result}, expected {expected}")
        return False
    return True

# Test cases
tests = [
    ("aaba", 8),
    ("aaaa", 4), 
    ("abc", 6),
    ("a", 1),
    ("abab", 7),
    ("abcd", 10),
    ("abcdefghij", 55),  # 10 chars: 10*11/2 = 55
]

all_passed = True
for s, expected in tests:
    if not test_case(s, expected):
        all_passed = False

if all_passed:
    print("\nAll tests passed! ✅")
else:
    print("\nSome tests failed! ❌")