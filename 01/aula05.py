velocidade = int(input('Digite a velocidade do carro: '))

if velocidade > 110:
    multa = (velocidade - 110) * 5
    print ('Você foi multado no valor de %5.2f' %multa)
else:
    print('Você não foi multado')
