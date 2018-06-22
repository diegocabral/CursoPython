i = 1
vetor = []

while i <= 10:
    n = str(input('Digite uma letra: '))
    vetor.append(n)
    i = i + 1

i = 0
qtd = 0
while i <= 9:
    if vetor[i] not in 'aeiou':
        qtd = qtd + 1
    i = i + 1
    
print ('Foram lidas %d consoantes' %qtd)

