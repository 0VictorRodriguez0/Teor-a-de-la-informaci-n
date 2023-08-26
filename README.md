# Esquema de la comunicación
Emitar la transferencia de paquetes con las 5 fases de un esquema de comunicación, el usuario ingresa el mensaje escrito y recibe el mensaje despues de pasar por las fases

## Fuentes de información:
Mensaje escrito por el usuario

## Transmisor:
El mensaje ingresado se guarda en una lista en donde cada posición representa un caracter, los datos pasan a un proceso de conversión binaria para luego ser enpaquetado con un Header y un Tail.

##Canal:
El canal por el cual sera transmitido es la fibra optica con una posibilidad de ruido en cada caracter en consecuencia a un proceso de selección aleatoria

##Receptor:
Recibe los datos y revisa que esten enpaquetados,si los datos son enpaquetados los convierte de binario a ASCII y los guarda en una lista, en caso de no ser enpaquetados, no se guardan los datos.

##Destino:
mensaje completo en formato ASCII escrito por el usuario inicial
