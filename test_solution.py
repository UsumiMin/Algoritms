import sys
from io import StringIO

# Import the solve function from our working solution
exec(open('/workspace/working_solution.py').read())

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
    ("a" * 100, 100),  # For "aaaa...a" with 100 a's, unique substrings = 100
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