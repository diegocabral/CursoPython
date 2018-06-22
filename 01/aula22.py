notas = []
soma = 0
i = 1

while i <= 4:
    n = float(input('Digite a nota: '))
    notas.append(n)
    soma = soma + n
    i = i + 1

print ('Notas: ', notas)
print ('Media: %4.2f' %(soma / 4))
    
