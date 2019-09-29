s = input()
maxk = 0
for i in range(len(s) // 2):
    k = 1
    for j in range(i + 1, len(s), i + 1):
        if s[:i + 1] == s[j:j + i + 1]:
            k += 1
        else:
            k = 1
            break
    if k > maxk:
        maxk = k
print(maxk)