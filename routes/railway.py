from typing import List, Dict
import itertools


# def solve_railway_helper(array: List[int], target: int) -> int:
#     sign: int = 1
#     # array: List[int] = sorted(array)

#     if target < 0:
#         array = reversed(array)
#         sign = -1

#     last_index: Dict[int, List[int]] = {
#         0: [-1]
#     }

#     for i in range(len(array)):
#         for s in list(last_index.keys()):
#             new_s: int = s + array[i]

#             if 0 < (new_s - target) * sign:
#                 pass
#             elif new_s in last_index:
#                 last_index[new_s].append(i)
#             else:
#                 last_index[new_s] = [i]

#     def recur(new_target: int, max_i: int) -> List[int]:
#         for i in last_index[new_target]:
#             if i == -1:
#                 yield []
#             elif max_i <= i:
#                 break
#             else:
#                 for ans in recur(new_target - array[i], i):
#                     ans.append(array[i])
#                     yield ans

#     for ans in recur(target, len(array)):
#         yield ans

# def countWays(arr, m, N):
 
#     count = [0 for i in range(N + 1)]
     
#     # base case
#     count[0] = 1
     
#     # Count ways for all values up
#     # to 'N' and store the result
#     for i in range(1, N + 1):
#         for j in range(m):
 
#             # if i >= arr[j] then
#             # accumulate count for value 'i' as
#             # ways to form value 'i-arr[j]'
#             if (i >= arr[j]):
#                 count[i] += count[i - arr[j]]
     
#     # required number of ways
#     return count[N]



# def solve_railway(in_str_ls: List[str]) -> List[str]:
#     '''
#     // Input JSON:
#     [
#     "5, 3, 2, 1, 4",
#     "3, 3, 4, 1, 2",
#     "11, 1, 2"
#     ]

#     // Output JSON:
#     [4, 2, 0]
#     '''
#     out: List[int] = []

#     for in_str in in_str_ls:
#         splitted_str: List[int] = [int(i.strip(",")) for i in in_str.split()]

#         target_len: int = splitted_str[0]
#         total_num_pieces: int = splitted_str[1]
#         piece_lengths: List[int] = splitted_str[2:]

#         print(f"target len: {target_len}")
#         print(f"num pieces: {total_num_pieces}")
#         print(f"piece lengths: {piece_lengths}")

#         # print(countWays(piece_lengths, total_num_pieces, target_len))
        

def solve_railway_final(in_str_ls: List[str]) -> List[str]:
    '''
    // Input JSON:
    [
    "5, 3, 2, 1, 4",
    "3, 3, 4, 1, 2",
    "11, 1, 2"
    ]

    // Output JSON:
    [4, 2, 0]
    '''
    result = []
    for strList in in_str_ls:
        strListSplit = strList.split(',')
        length = int(strListSplit[0])
        types = int(strListSplit[1])
        pieces = [int(i) for i in strListSplit[2:]]

        dp = [0] * (length + 1)
        dp[0] = 1

        for piece in pieces:
            for i in range(piece, length + 1):
                dp[i] += dp[i - piece]
        
        result.append(dp[length])
    
    return result

print(solve_railway_final([
  "5, 3, 2, 1, 4",
  "3, 3, 4, 1, 2",
  "11, 1, 2"
]))

if __name__ == '__main__':
    solve_railway_final(
        [
        "5, 3, 2, 1, 4",
        "3, 3, 4, 1, 2",
        "11, 1, 2"
        ]
    )