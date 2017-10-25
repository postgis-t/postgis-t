# postgis-t
A SpatioTemporal PostgreSQL Database Extension

# Dirétorio 'database schema'
Contém o schema do banco de dados a ser criado no PostgreSQL para
os testes com dos dados de trajetória

# Diretório 'script'
Dois scripts usados para carregar os dados da boia.
     
	-- getBouyData.py
		Usado para carregar os dados da tabela buoy_data_buoy. Para carregar os dados, é passado os links aonde estão armazenados estes dados no servidor FTP. Sendo estes links: ftp://ftp.aoml.noaa.gov/pub/phod/buoydatadirfl_5001_10000.dat,ftp://ftp.aoml.noaa.gov/pub/phod/buoydata/dirfl_10001_15000.dat,ftp://ftp.aoml.noaa.gov/pub/phod/buoydata/dirfl_15001_jun17.dat,ftp://ftp.aoml.noaa.gov/pub/phod/buoydata/dirfl_1_5000.dat
		Caso de algum problema, por favor entrar no link 'ftp://ftp.aoml.noaa.gov/pub/phod/buoydata/' e trocar o link do script, pois pode acontecer casos de atualizarem os repositórios e assim o link desaparecer, mudando para um novo nome.
	
	-- getTrajectoryData.py
		Usado para carregar os dados da tabela traj_buoy_trajectory. Para carregar os dados, é necessário passar via terminal o diretório aonde o arquivo dos dados da trajetória está armazenado. É necessário baixar os arquivos do repositório FTP: ftp://ftp.aoml.noaa.gov/pub/phod/buoydata/.
		Até o presente momento (16/10/2017) os arquivos presentes são:
		buoydata_10001_15000.dat.gz, buoydata_15001_jun17.dat.gz,
		buoydata_15001_mar17.dat.gz, buoydata_15001_sep16.dat.gz, 
		buoydata_1_5000.dat.gz e buoydata_5001_10000.dat.gz


