# Alexas HeadBleed
=========

Alexas HeadBleed permite detectar la vulnerabilidad HeadBleed en los dominios más visitados según el ranking de Alexas. Se puede mirar tanto por el ranking global como por Paises.
También puede pasarle un fichero con urls para que detecte si también son dominios vulnerables.


Instrucciones
------------
Hay 4 opciones:

- python main.py
    > Crea un fichero que contiene todos los paises con dominios vulnerables dentro del top 500 por país del ranking de Alexas, con el número total de dominios vulnerables y éstos.

- python main.py -g X
    > Crea un fichero que contiene el total de dominios vulnerables dentro del top X global del ranking de Alexas, con el número total de dominios vulnerables y éstos.

- python main.py -c X
    > Crea un fichero que contiene los paises con dominios vulnerables dentro del top X por país del ranking de Alexas, con el número total de dominios vulnerables y éstos.

- python main.py -f FilePath
    > Crea un fichero que contiene dominios vulnerables dentro del fichero FilePath, con el número total de dominios vulnerables y éstos.


El fichero FilePath debe ser un fichero con una url por linea y si se quiere, especificar el puerto:

```
dominio1.com
dominio2.org
dominioconpuerto.net 442
. . .
```

Dependencias
------------
* Python 2 (2.7 should be sufficient)
* [BeautifulSoup](https://pypi.python.org/pypi/BeautifulSoup/3.2.1) version 3.2.1

License
-------
Esta obra está sujeta a la licencia [Reconocimiento-NoComercial 4.0 Internacional de Creative Commons](http://creativecommons.org/licenses/by-nc/4.0/). Para ver una copia de esta licencia, visite visite[http://creativecommons.org/licenses/by-nc/4.0/](http://creativecommons.org/licenses/by-nc/4.0/).


Como puede ayudar
----------------

Si encuentra cualquier error o problema puede [contactar conmigo en Twitter](https://twitter.com/miqueltur) o por [email](mailto:miquel.tur.m@gmail.com).