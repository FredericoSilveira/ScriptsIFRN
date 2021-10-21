import csv
import re

#ramais = ['9845','9846','9847','9849','9850','9854','9851','9852','9853','9857','9858','9859']
#periodos = ['05-2013','06-2013','07-2013','08-2013']
ramais = ['9868','9870']
periodos = ['09-2018','10-2018','11-2018','12-2018']
fi = open('/Users/fred/Downloads/ILZA_recebido.csv', 'w')
fi.write("Origem, Destino, Permissoes, Data Chamada, Hora Chamada, Inicio Conversacao, Final Conversacao, Duracao Ligacao, Duracao Conversacao\n")
for periodo in periodos:
    with open('/Users/fred/Downloads/Master.csv', 'r') as f:
        reader = csv.reader(f)
        print(periodo)
        for row in reader:
            data = (row[9].split()[0]).split('-')
            datafinal = str(data[1]) + "-" + str(data[0])
            if datafinal == str(periodo):
                for ramal in ramais:
                    # 1 para chamadas efetuadas e 2 para chamadas recebidas
                    if (ramal == str(row[2])) and (str(row[14]) == 'ANSWERED'):
                        fi.write(str(row[1]) + ", "  + str(row[2]) + ", " + str(row[3]) + ", " + str(data[2]) + "/" + str(data[1]) + "/" + str(data[0]) + ", " + ((row[9].split()[1]).split(':'))[0] + ", " + (row[10].split()[1]) + ", " + (row[11].split()[1]) + ", " + str(row[12]) + ", " + str(row[13]) + "\n")

fi.close()
