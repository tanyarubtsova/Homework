'''
 task 2, program 2
'''
d = dict()
s = input()
while s != "":
    s += ' '
    word = ''
    for i in s.split(' '):
        if d.get(i) is None:
            d[i] = 1
        else:
            d[i] += 1
    s = input()
ans_word = '-'
max_num = 0
for i in d:
    if d[i] > max_num:
        max_num = d[i]
        ans_word = i
    elif d[i] == max_num:
        ans_word = '-'
print(ans_word)


