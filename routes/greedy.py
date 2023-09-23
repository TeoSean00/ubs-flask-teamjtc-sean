import json
import logging
from typing import List

from flask import request, Response

from routes import app

logger = logging.getLogger(__name__)


@app.route('/greedymonkey', methods=['POST'])
def solve_greedy():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    w: int = data.get("w")
    v: int = data.get("v")
    f: List[List[int]] = data.get("f")
    
    res: int = greedyMonkey(w, v, f)
    logging.info("My result :{}".format(res))
    return str(res)


def greedyMonkey(w, v, f):
    dp = [[0] * (v + 1) for _ in range(w + 1)]
    for i in range(len(f)):
        weight, volume, value = f[i]
        for j in range(w, weight - 1, -1):
            for k in range(v, volume - 1, -1):
                dp[j][k] = max(dp[j][k], dp[j - weight][k - volume] + value)
    return dp[w][v]