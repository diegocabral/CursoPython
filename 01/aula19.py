notas = [5, 6, 7, 8, 9]
soma = 0
x = 0
while x < 5:
    soma = soma + notas[x]
    x = x + 1
print ('Media: %5.2f' %(soma / x))
