import json
import logging
from typing import Dict, List

from flask import request

from routes import app

logger = logging.getLogger(__name__)
        
@app.route('/railway-builder', methods=['POST'])
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