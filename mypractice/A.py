old, new = [], []
for i in range(int(raw_input())):
    inp = list(map(int,raw_input().split()))
    if inp[0] == 1:
        new.append(inp[1])
    elif inp[0] == 2:
        if not old :
            while new :
                old.append(new.pop())
            old.pop()
    else:
        print old[-1] if old else new[0]