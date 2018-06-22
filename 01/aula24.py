texto = str(input('Digite uma palavra: '))

if texto == texto[::-1]:
    print('Palavra palíndrome')
else:
    print('Palavra não palíndrome')
