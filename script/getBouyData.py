# coding=utf-8

import urllib.request
import psycopg2 as psy

#Este try exception e responsavel por garantir que exista uma conexao com o banco de dados
#Caso o banco de dados nao exista ou por algum motivo ele nao esteja conectado,
# o ira entrar numa exceção que alem de mostrar o erro para o usuario, ira encerrar o processo.
try:
    connection = psy.connect(database="buoy2", user="postgres", password="root", host="127.0.0.1", port="5432")
except Exception as a:
    print(a)
    exit()


#Esta e a estrutura do sql a ser salva no banco de dados
#substituindo as chaves pelos dados da boia.
sql = "INSERT INTO BUOY_DATA_BUOY VALUES ({}, {}, {}, '{}', NULLIF('{} {}', '0000/00/00 00:00')::timestamp," \
      "ST_GeomFromText('POINT({} {})', 4326), NULLIF('{} {}', '0000/00/00 00:00')::timestamp, " \
      "ST_GeomFromText('POINT({} {})', 4326), NULLIF('{} {}','0000/00/00 00:00')::timestamp, {})"


#Essa função e responsavel por juntar os dados da boia que foram pego do servidor ftp, estruturar dentro da variavel sql
# e armazena los no banco de dados.
#Para tentar minimizar a demora no armazenamento os dados serao mantidos em cache, pois sao muitos dados, contudo
#  foi colocado um 'if i % 1000 == 10000' que ao chegar no valor de 10 mil registros, eles serao carregados no banco
def insertDB(connection, sql, argv):
    try:
        with connection.cursor() as cursor:
            for i, line in enumerate(argv):

                fields = line.strip().split()
                cursor.execute(sql.format(fields[0], fields[1], fields[2], fields[3],
                                          fields[4], fields[5], fields[6], fields[7],
                                          fields[8], fields[9], fields[10], fields[11],
                                          fields[12], fields[13], fields[14]))

                if i % 1000 == 10000:
                    connection.commit()

        connection.commit()

    except IOError as error:
        print(error)



#Uma lista de link com os dados da boia que estao armazenados no servidor ftp.

links = ['ftp://ftp.aoml.noaa.gov/pub/phod/buoydata/dirfl_5001_10000.dat','ftp://ftp.aoml.noaa.gov/pub/phod/buoydata/dirfl_10001_15000.dat'\
         'ftp://ftp.aoml.noaa.gov/pub/phod/buoydata/dirfl_15001_jun17.dat','ftp://ftp.aoml.noaa.gov/pub/phod/buoydata/dirfl_1_5000.dat']


#Nesse bloco de codigo um 'for' ira varrer a lista de links e capturar os dados que estao presentes no servidor ftp
#assim caso nao ocorra nenhum problema, estes dados serao transformados em um array e mandados para a funcao 'insertDB()'
#para que eles sejam armazenados no banco de dados.

for link in links:

    try:
        bouyData = urllib.request.urlopen(link).read().decode('utf-8')

    except urllib.HTTPError as error:
        print('HTTPError = ' + str(error.code))
        continue

    except urllib.URLError as error:
        print('URLError = ' + str(error.reason))
        continue

    bouyDataFormatArray = bouyData.split("\n")

    #Detalhe para o 'bouyDataFormatArray[:-1]'
    #Como foi descoberto, sempre o ultimo valor do array dos dados da boia sera vazio.
    #Entao para evitar problemas ou aumento de codigo desnecessario, o ultimo valor e ignorado.
    insertDB(connection, sql, bouyDataFormatArray[:-1])

