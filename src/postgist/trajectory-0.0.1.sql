
/* Função 'mensuare' retorna a posição (x e y, [x] e [y]) de uma trajetoria 
referente a uma data.
Ex: mensuare('10-05-2010')
	return Geometry('POINT(44 44)')
	or return Geometry('LINESTRING(44 44, 44 44, 44 44)')
	etc...
*/
CREATE OR REPLACE FUNCTION measure(t trajectory, ts timestamp)
RETURNS geometry AS
$$

$$
LANGUAGE plpython3u

/* Essa função retorna o objeto geometry (conjunto de Xs e Ys)
ou o objeto trajetoria
*/
CREATE OR REPLACE FUNCTION positions()
RETURNS geometry AS
$$

$$
LANGUAGE plpython3u

/* Retorna a primeira data de uma trajetoria*/
CREATE OR REPLACE FUNCTION begins(t trajectory)
RETURNS timestamp AS
$$

$$
LANGUAGE plpython3u


/* Retorna a ultima data de uma trajetoria*/
CREATE OR REPLACE FUNCTION ends(t trajectory)
RETURNS timestamp AS
$$

$$
LANGUAGE plpython3u


/* Retorna o máximo e o minimo de X e Y
*/
CREATE OR REPLACE FUNCTION boundary(t trajectory)
RETURNS timestamp AS
$$

$$
LANGUAGE plpython3u


/* Retorna uma trajetória com todos os pontos que estão depois de uma data
caso o valor estiver fora do range, a função irá retorna null

traj.time = ['10-05-2014 14:15:18','10-05-2014 14:15:19','10-05-2014 14:15:20']
traj.x = [1,2,3]
traj.y = [5,4,8]

Ex: select after( traj, '10-05-2014 14:15:18' )
	return [(2,4),(3,8)]
*/
CREATE OR REPLACE FUNCTION after(t trajectory, ts timestamp)
RETURNS geometry AS
$$

$$
LANGUAGE plpython3u

/* Retorna uma trajetória com todos os pontos que estão antes de uma data
caso o valor estiver fora do range, a função irá retorna null

traj.time = ['10-05-2014 14:15:18','10-05-2014 14:15:19','10-05-2014 14:15:20']
traj.x = [1,2,3]
traj.y = [5,4,8]

Ex: select after(  traj, '10-05-2014 14:15:20' )
	return [(1,5),(2,4)]
*/
CREATE OR REPLACE FUNCTION before(t trajectory,ts timestamp)
RETURNS geometry AS
$$
	print('')
$$
LANGUAGE plpython3u

/* Retorna uma trajetória com todos os pontos que esteja entre duas data
caso o valor estiver fora do range, a função irá retorna null

traj.time = ['10-05-2014 14:15:18','10-05-2014 14:15:19','10-05-2014 14:15:20']
traj.x = [1,2,3]
traj.y = [5,4,8]

Ex: select after(  traj, '10-05-2014 14:15:18' , '10-05-2014 14:15:20' )
	return [(1,5),(2,4)]
*/
CREATE OR REPLACE FUNCTION during(t trajectory,ts1 timestamp, ts2 timestamp)
RETURNS geometry AS
$$
	print('')
$$
LANGUAGE plpython3u


/* Essa função retorna um array de trajetorias que esteja intersectando uma geometria passada
Ex:
		_____________________________________________
		|					    |
		|					    |
		|					    |
		|					    |
		|					    |
		|					    |	    _________
		|				____________|______|
		|			       |	    |
		|			       |	    |
		|       Segundo array ----->   |	    |
		|			       |	    |
		|			       |	    |
		|			       |____________|_____
		|					    |     |
		|					    |	  |
		|					    |	  | 	
		|				      ______|_____|
		|	  ____________________________|	    |
		|    	  |			    	    |
		|	  |				    |
		|     	  |   <---- Primeiro array    	    |
		|    	  |			    	    |
		|	  |				    |
		|    _____|			    	    |
	________|___|					    |
	|	|					    |
	|	|					    |
		|___________________________________________|
		
*/
CREATE OR REPLACE FUNCTION intersection(t trajectory, g geometry) 
RETURNS geometry AS
$$
	print('')
$$
LANGUAGE plpython3u


/* Essa função retorna um array de trajetorias que esteja fora uma geometria passada
Ex:
		_____________________________________________
		|					    |
		|					    |
		|					    |
		|					    |
		|					    |
		|					    |	    _________  <--- Terceiro Array
		|				____________|______|
		|			       |	    |
		|			       |	    |
		|       		       |	    |
		|			       |	    |
		|			       |	    |
		|			       |____________|_____
		|					    |     |
		|					    |	  |
		|					    |	  | <--- Segundo Array
		|				      ______|_____|
		|	  ____________________________|	    |
		|    	  |			    	    |
		|	  |				    |
		|     	  |   			   	    |
		|    	  |			    	    |
		|	  |				    |
Primeiro Array	|    _____|			    	    |
  | 	________|___|					    |
  |--->	|	|					    |
     	|	|					    |
		|___________________________________________|
		
*/
CREATE OR REPLACE FUNCTION difference(t trajectory, g geometry) 
RETURNS geometry AS
$$
	print('')
$$
LANGUAGE plpython3u
