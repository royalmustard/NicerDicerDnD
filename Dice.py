import random

def D(die, rolls=1):
    result = 0
    if rolls < 1:
        return None
    else:
        for i in range(0,rolls):
            result += random.randint(1, die)
        return result
