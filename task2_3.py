'''
task 2, program 3
Example_1:
    Input: 23
    Output: ["ad""ae""af""bd""be""bf""cd""ce""cf"]
Example_2:
    Input: 14
    Output: ["g""h""i"]
'''
dict = (
    (' '), #0
    (''), #1
    ('a', 'b', 'c'), #2
    ('d', 'e', 'f'),
    ('g', 'h', 'i'),
    ('j', 'k', 'l'),
    ('m', 'n', 'o'),
    ('p', 'q', 'r', 's'),
    ('t', 'u', 'v'),
    ('w', 'x', 'y', 'z') #9
)

def gen(num, s, i, n, count_of_1):
    if i == n:
        print('"' + s + '"', end='')
        return
    else:
        while int(num[i]) == 1:
            i += 1
            count_of_1 += 1
        for j in dict[int(num[i])]:
            s += j
            gen(num, s, i + 1, n, count_of_1)
            if count_of_1 > 0:
                s = s[:(i - count_of_1)]
            else:
                s = s[:i]


num = input()
s = ''
print('[', end='')
n = len(num)
while num[n - 1] == '1':
    n -= 1
gen(num, s, 0, n, 0)
print(']', end='')
