def debug_solve(s):
    """Debug version of the algorithm"""
    n = len(s)
    if n == 0:
        return 0
    
    print(f"Input: '{s}', length: {n}")
    
    # Manual calculation of unique substrings for verification
    substrings = set()
    for i in range(n):
        for j in range(i + 1, n + 1):
            substrings.add(s[i:j])
    print(f"All unique substrings: {sorted(substrings)}")
    print(f"Count: {len(substrings)}")
    
    # Now use suffix array method
    s_num = [ord(c) for c in s]
    
    # Initialize suffix array with indices
    sa = list(range(n))
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
        sa[cnt[s_num[i]]] = i
        cnt[s_num[i]] += 1
    
    print(f"After first sort, sa: {sa}")
    
    # Assign initial ranks
    r = 0
    for i in range(n):
        if i > 0 and s_num[sa[i]] != s_num[sa[i-1]]:
            r += 1
        rank[sa[i]] = r
    
    print(f"Initial ranks: {rank}")
    
    # Doubling algorithm to build suffix array
    k = 1
    iteration = 0
    while k < n and r < n - 1:
        print(f"Iteration {iteration}: k={k}, r={r}")
        
        # Radix sort by pair (rank[i], rank[i+k])
        # First sort by second element of the pair
        cnt = [0] * (r + 2)
        for i in range(n):
            second = rank[sa[i] + k] if sa[i] + k < n else 0
            cnt[second] += 1
        
        for i in range(1, len(cnt)):
            cnt[i] += cnt[i - 1]
        
        new_sa = [0] * n
        for i in range(n-1, -1, -1):
            second = rank[sa[i] + k] if sa[i] + k < n else 0
            cnt[second] -= 1
            new_sa[cnt[second]] = sa[i]
        
        sa = new_sa
        print(f"After sorting by second element: sa={sa}")
        
        # Now sort by first element of the pair
        cnt = [0] * (r + 2)
        for i in range(n):
            first = rank[sa[i]]
            cnt[first] += 1
        
        for i in range(1, len(cnt)):
            cnt[i] += cnt[i - 1]
        
        new_sa = [0] * n
        for i in range(n-1, -1, -1):
            first = rank[sa[i]]
            cnt[first] -= 1
            new_sa[cnt[first]] = sa[i]
        
        sa = new_sa
        print(f"After sorting by first element: sa={sa}")
        
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
        print(f"Updated ranks: {rank}")
        k *= 2
        iteration += 1
    
    print(f"Final suffix array: {sa}")
    print("Suffixes in sorted order:")
    for idx in sa:
        print(f"  s[{idx}:] = '{s[idx:]}'")
    
    # Calculate LCP array using Kasai's algorithm
    lcp = [0] * n
    rank_pos = [0] * n  # position of suffix starting at i in the sorted suffix array
    for i in range(n):
        rank_pos[sa[i]] = i
    
    print(f"rank_pos array: {rank_pos}")
    
    h = 0
    for i in range(n):
        if rank_pos[i] > 0:
            j = sa[rank_pos[i] - 1]  # previous suffix in sorted order
            # Compute LCP between s[i:] and s[j:]
            old_h = h
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rank_pos[i]] = h
            print(f"LCP between '{s[i:]}' and '{s[j:]}' = {h}")
            if h > 0:
                h -= 1
    
    print(f"LCP array: {lcp}")
    
    # Total unique substrings = total possible substrings - sum of LCP values
    total_possible = n * (n + 1) // 2
    total = total_possible
    for i in range(1, n):
        total -= lcp[i]
    
    print(f"Total possible: {total_possible}")
    print(f"Sum of LCP values (except lcp[0]): {sum(lcp[1:])}")
    print(f"Result: {total}")
    
    return total

# Test with "aaaa"
debug_solve("aaaa")
print("\n" + "="*50 + "\n")
debug_solve("aaba")