def nset(n):
    cnt = 0
    while n:
        cnt += n & 1
        n >>= 1
    return cnt

def num2lex(lst):
    def key(n):
        return [ nset(n), -n ]
    return sorted(lst,key=key)

def lex2num(lst):
    lexlist = num2lex(list(range(len(lst))))
    enumlist = list(zip(lexlist,lst))
    return [x[1] for x in sorted(enumlist,key = lambda x:x[0])]
