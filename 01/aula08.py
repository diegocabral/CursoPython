n1 = int(input('Digite o numero 1: '))
n2 = int(input('Digite o numero 2: '))
n3 = int(input('Digite o numero 3: '))

if n1 >= n2 and n1 >= n3:
    print('Primeiro: %d' %n1)
elif n2 >= n3:
    print('Segundo: %d' %n2)
else:
    print('Terceiro: %d' %n3)
