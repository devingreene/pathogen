def nset(n):
    cnt = 0
    while n:
        cnt += n & 1
        n >>= 1
    return cnt

def bitlength(n):
    res = -1
    while n:
        res += 1
        n >>= 1
    return res
