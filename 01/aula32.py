"Minha resolução"

import random
palavra = list(input('Digite um palavra: '))
random.shuffle(palavra)
print (''.join(palavra))

"Resolução do curso"

def embaralha(s):
    import random
    lista = list(s)
    random.shuffle(lista)
    return ''.join(lista)
