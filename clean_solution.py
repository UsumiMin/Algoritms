import time
import tracemalloc

tracemalloc.start()

def solve(s):
    """Count unique substrings using suffix array and LCP"""
    n = len(s)
    if n == 0:
        return 0
    
    # Convert string to numbers for efficient processing
    s_nums = [ord(c) for c in s]
    
    # Build suffix array using the doubling algorithm
    sa = list(range(n))
    rank = [0] * n
    
    # Initialize ranks by first character
    max_char = max(s_nums) if s_nums else 0
    cnt = [0] * (max_char + 2)
    
    for i in range(n):
        cnt[s_nums[i] + 1] += 1
    
    for i in range(1, len(cnt)):
        cnt[i] += cnt[i - 1]
    
    for i in range(n):
        cnt[s_nums[i]] += 1
        sa[cnt[s_nums[i]] - 1] = i  # Place in correct position
    
    # Fix the counting sort
    cnt = [0] * (max_char + 1)
    for i in range(n):
        cnt[s_nums[i]] += 1
    
    pos = 0
    for i in range(len(cnt)):
        for j in range(cnt[i]):
            sa[pos] = s_nums.index(i, sa[pos] if pos < len(sa) and sa[pos] < len(s_nums) else 0) if i in s_nums else 0
            # Actually, let's fix this properly:
    
    # Correct counting sort for first character
    sa = list(range(n))
    cnt = [0] * (max_char + 1)
    
    for i in range(n):
        cnt[s_nums[i]] += 1
    
    for i in range(1, len(cnt)):
        cnt[i] += cnt[i - 1]
    
    temp_sa = [0] * n
    for i in range(n-1, -1, -1):  # Stable sort
        cnt[s_nums[i]] -= 1
        temp_sa[cnt[s_nums[i]]] = i
    
    sa = temp_sa[:]
    
    # Assign initial ranks
    r = 0
    rank[sa[0]] = 0
    for i in range(1, n):
        if s_nums[sa[i]] != s_nums[sa[i-1]]:
            r += 1
        rank[sa[i]] = r
    
    # Doubling algorithm
    k = 1
    tmp_rank = [0] * n
    
    while k < n and r < n - 1:
        # Sort by second element of (rank[i], rank[i+k])
        # Use counting sort with pairs
        cnt = [0] * (r + 1)
        for i in range(n):
            cnt[rank[i]] += 1
        for i in range(1, len(cnt)):
            cnt[i] += cnt[i - 1]
        
        new_sa = [0] * n
        # Sort by second element (rank[i+k]) first
        for i in range(n):
            second_rank = rank[sa[i] + k] if sa[i] + k < n else -1
            # For this, we need to sort by (rank[i+k], rank[i]) pairs, not (rank[i], rank[i+k])
            # Let's restructure the algorithm
            pass
        
        # Actually, let's implement a clean version of the SA-IS algorithm approach
        # Or just use a correct implementation of the standard doubling algorithm
        aux_sa = [0] * n
        cnt2 = [0] * (r + 1)
        
        # Count occurrences of second element
        for i in range(n):
            if sa[i] + k < n:
                cnt2[rank[sa[i] + k]] += 1
            else:
                cnt2[0] += 1  # -1 maps to 0 in counting
        
        # Convert to cumulative count
        for i in range(1, len(cnt2)):
            cnt2[i] += cnt2[i - 1]
        
        # Build aux_sa by sorting by second element (stable)
        for i in range(n-1, -1, -1):
            if sa[i] + k < n:
                pos = cnt2[rank[sa[i] + k]]
                cnt2[rank[sa[i] + k]] -= 1
            else:
                pos = cnt2[0]
                cnt2[0] -= 1
            aux_sa[pos - 1] = sa[i]
        
        # Now sort by first element (stable)
        cnt = [0] * (r + 1)
        for i in range(n):
            cnt[rank[aux_sa[i]]] += 1
        for i in range(1, len(cnt)):
            cnt[i] += cnt[i - 1]
        
        for i in range(n-1, -1, -1):
            pos = cnt[rank[aux_sa[i]]]
            cnt[rank[aux_sa[i]]] -= 1
            sa[pos - 1] = aux_sa[i]
        
        # Update ranks based on pairs
        tmp_rank[sa[0]] = r = 0
        for i in range(1, n):
            # Compare pairs (rank[sa[i-1]], rank[sa[i-1]+k]) and (rank[sa[i]], rank[sa[i]+k])
            prev_pair = (rank[sa[i-1]], rank[sa[i-1] + k] if sa[i-1] + k < n else -1)
            curr_pair = (rank[sa[i]], rank[sa[i] + k] if sa[i] + k < n else -1)
            
            if prev_pair != curr_pair:
                r += 1
            tmp_rank[sa[i]] = r
        
        rank, tmp_rank = tmp_rank, rank
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

def main():
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