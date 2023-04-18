def get_values(line):
    # divide a linha em colunas separadas pelo caractere '|'
    columns = line.strip().split('|')

    # retorna o valor da terceira coluna como uma string
    return columns[2]


# lê as linhas do arquivo1.txt e armazena os valores da terceira coluna em um conjunto
with open('/Users/fred/Downloads/arquivo1.txt', 'r') as f1:
    values1 = set(get_values(line) for line in f1 if line.startswith('31|'))

# abre os arquivos de entrada e saída
with open('/Users/fred/Downloads/arquivo1.txt', 'r') as f1, open('/Users/fred/Downloads/arquivo2.txt', 'r') as f2, \
        open('/Users/fred/Downloads/output1.txt', 'w') as out1, open('/Users/fred/Downloads/output2.txt', 'w') as out2:
    # lê as linhas do arquivo2.txt
    for line in f2:
        if line.startswith('30|'):
            # se a linha começa com '30', insere no output1.txt
            out1.write(line)
        elif line.startswith('31|'):
            # se a linha começa com '31', verifica se o valor da terceira coluna está em values1
            value = get_values(line)
            if value not in values1:
                out1.write(line)
                # se o valor não for encontrado em values1, ignora todas as linhas subsequentes começando com '32'
                for line in f2:
                    if line.startswith('32|'):
                        continue
                    else:
                        break
            else:
                # se o valor for encontrado em values1, insere todas as linhas subsequentes começando com '32' no output2.txt
                out2.write(line)
                for line in f2:
                    if line.startswith('32|'):
                        out2.write(line)
                    else:
                        break
