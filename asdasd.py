
import numpy as np
import random 

def _by_age(age, min, max, median_age):
    avg = max * np.exp(-0.5 * ((age - median_age) / 6)**2)
    return int(np.clip(np.random.normal(avg, 8), min, max))

age = 25
games = _by_age(age, 1, 50, 27)
expected_goals = 0.4 * games
print(age, games, expected_goals)
goals = _by_age(age, 5, 50, 27)
