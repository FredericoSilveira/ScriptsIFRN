import csv
import re

fi = open('/Users/fred/Downloads/censup-vinculos.txt', 'w')
fi.write('40|1082')
is41 = False
is42 = False
linha = ''
quantidade = 0

with open('/Users/fred/Downloads/CENSUP-GERAL.txt', 'r') as f:
    for line in f:
        l = line.rstrip()
        print('***********')
        print(l)
        print('***********')
        if l.startswith('41'):
            if quantidade > 1:
                fi.write(linha)
                print('--------------------')
                print(quantidade)
                print(linha)
                print('--------------------')
                linha = ''
                quantidade = 0
            quantidade = 0
            linha = '\n'+ l
            is41 = True
            is42 = False
        if l.startswith('42') and is42 == True:
            linha = linha + '\n' + l
            quantidade += 1
        if l.startswith('42') and is41 == True:
            is41 = False
            is42 = True
            linha = linha + '\n' + l
            quantidade += 1

fi.close()

