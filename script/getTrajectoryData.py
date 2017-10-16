# requires activate py34

import psycopg2 as psy
import sys
import numpy as np

#Estrutura em sql a ser salva no banco de dados
#substituindo as chaves pelos dados da boia.
sql = "INSERT INTO TRAJ_BUOY_TRAJECTORY (traj_buoy_id, traj_date, \
traj_position_time,traj_location,traj_celsius_temperature,traj_east_velocity,\
traj_north_velocity,traj_speed_velocity,traj_variance_location ,traj_variance_temp)\
 VALUES ({}, NULLIF('{}/{}/{}', '0000/00/00 00:00')::timestamp, {},\
 ST_GeomFromText('POINT({} {})', 4326), {}, {}, {}, {}, ST_GeomFromText('POINT({} {})', 4326), {})"


#Este try exception e responsavel por garantir que exista uma conexao com o banco de dados
#Caso o banco de dados nao exista ou por algum motivo ele nao esteja conectado,
# o ira entrar numa exceção que alem de mostrar o erro para o usuario, ira encerrar o processo.
try:
    connection = psy.connect("dbname='bouy' user='postgres' host='localhost' password='root' port=5432")
except:
    print("Unable to connect to the database.")
    exit()


#Este script ira receber atraves da linha de comando o caminho da onde o arquivo CSV se encontra,
#Assim esse if ira verificar, se e somente se, recebeu um parametro de entrada.
#Mais do que isso ele ira informar um erro e ira encerrar o processo
if len(sys.argv) != 2:
    print("Usage: {} <csv_file_path>.".format(sys.argv[0]))
    exit()


#Neste try ele ira pegar o parametro de entrada da linha de comando e ira tentar acessar o arquivo para a captura dos dados.
#Ele ira varrer o arquivo pegando linha por linha, e colocando na variavel 'fields' os dados da linha estruturado
# dentro de um array. Assim e formatado os campos seguindo a ordem que foi pensada antes na criação do banco de dados
# e armazena na memoria cache. Com um grande volume de dados, foi utilizado um  if que ao chegar no valor de 10 mil registros,
# eles serao carregados no banco.
try:
    with open(sys.argv[1], 'r') as data:
        with connection.cursor() as cursor:
            for i, line in enumerate(data):
                fields = line.strip().split()

                cursor.execute(sql.format(fields[0], fields[3], fields[1], str(np.float32(fields[2]).astype(int)),
                                 str((float(fields[2]) % 1) * 1000), fields[4], fields[5], fields[6], fields[7],
                                 fields[8], fields[9], fields[10], fields[11], fields[12]))

                if i % 1000 == 10000:
                    connection.commit()

    connection.commit()
except FileNotFoundError:
    print("Error: File not found!")


