data = input('Digite uma data no formato dd/mm/aaaa: ')
dia, mes, ano = data.split('/')

meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio',
         'junho', 'julho', 'agosto','setembro', 'outubro',
         'novembro', 'dezembro']

print('%s de %s de %s' %(dia, meses[int(mes) - 1], ano))
