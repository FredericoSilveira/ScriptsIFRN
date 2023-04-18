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
    # flag para indicar se a última linha lida do arquivo2.txt foi uma linha 31 com valor não encontrado
    last_line_31_not_found = False

    # lê as linhas do arquivo2.txt
    for line in f2:
        if line.startswith('30|'):
            # se a linha começa com '30', insere no output1.txt
            out1.write(line)
            # reseta a flag para indicar que a última linha lida não foi uma linha 31 com valor não encontrado
            last_line_31_not_found = False
        elif line.startswith('31|'):
            # se a linha começa com '31', verifica se o valor da terceira coluna está em values1
            value = get_values(line)
            if value not in values1:
                out1.write(line)
                # define a flag para indicar que a última linha lida foi uma linha 31 com valor não encontrado
                last_line_31_not_found = True
            else:
                # se o valor for encontrado em values1, insere a linha no output2.txt
                out2.write(line)
                # reseta a flag para indicar que a última linha lida não foi uma linha 31 com valor não encontrado
                last_line_31_not_found = False
        elif line.startswith('32|'):
            # se a linha começa com '32', verifica se a flag de última linha 31 com valor não encontrado foi definida
            if last_line_31_not_found:
                # se a flag foi definida, escreve a linha no output1.txt e continua verificando as próximas linhas 32
                out1.write(line)
            else:
                # se a flag não foi definida, escreve a linha no output2.txt e continua verificando as próximas linhas 32
                out2.write(line)
        else:
            # ignora qualquer outra linha que não começa com '30|', '31|', ou '32|'
            continue
