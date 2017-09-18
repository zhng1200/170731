def isBalanced(str):
    M = '{[('
    N = '}])'
    arr=[]
    for i in str:
        if i in M:
            arr.append(i)
        else:
            if not len(arr) or i!=N[M.index(arr.pop())]:
                return "NO"
    if len(arr):
        return 'NO'
    else:
        return "YES"
if __name__ == "__main__":
    for a0 in range(int(raw_input().strip())):
        result = isBalanced(raw_input().strip())
        print result
def demo():
    pass