def fat(x):
    i = 1
    fat = 1
    while i < x:
        fat = fat * i
        i += 1
    return fat

for n in range(6):
    print(fat(n))
