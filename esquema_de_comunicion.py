# -*- coding: utf-8 -*-
"""Esquema de comunicion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AOsUFl83ufnTgiWYl9B6Jw23n4J7HHsG
"""

# pip install bitstring

"""# Esquema de comunicación"""

from bitstring import BitArray
import random
import time
import math
import random

#Entropia de shannon
def EntropiaConocida(probabilidad):
  E = -(math.log(probabilidad, 2))
  return E

def EntropiaAleatoria(probabilidades):
  k = len(probabilidades)
  suma = 0
  for i in range(0,k):
    # print(i)
    if probabilidades[i] > 0:
      Ek = probabilidades[i] * math.log(probabilidades[i], 2)
      suma = suma + Ek
  return -suma

#Fuente de información
#pide como entrada un mensaje
def Finformacin():

    nombre = str(input("Escribe tu mensaje "))
    return nombre

#pasa del string a una lista de caracteres
def separar(mensaje):
  lista = []
  for i in mensaje:
    lista.append(i)
  return lista

#convierte el mensaje a binario
def transmite(mensaje):
    # Convertir el mensaje en una secuencia de bits
    bitsM = BitArray(bytes=mensaje.encode('utf-8'))
    return bitsM.bin

#enpaqueta los datos con INIT al inicio y FIN al final de la cadena
def enpaquetar(cadena):
  pack = ["INI"]
  for i in range(len(cadena)):
    pack.append(cadena[i])
  pack.append("FIN")
  return pack

#Reproduce posible ruido sobre las cadenas de bits
#entra: palabra de 8 bits
#sale: palabra con 8 bits con posible cambio en alguno de los bits
def ruido(LetraBytes):
  causa = False
  letra = LetraBytes
  aleatorio1 = random.randint(1, 10)
  # aleatorio2 = random.randint(1, 5)
  if aleatorio1 < 3:
    causa = True
    aleatorioBytes = random.randint(0,7)
    # print(aleatorioBytes,letra[aleatorioBytes])
    if letra[aleatorioBytes] == "0":
      # print("cambio a 1",aleatorioBytes)
      letra = letra[:aleatorioBytes] + '1' + letra[aleatorioBytes + 1:]
    else:
      # print("cambio a 0",aleatorioBytes)
      letra = letra[:aleatorioBytes] + '0' + letra[aleatorioBytes + 1:]


  return letra,causa

#Crea ruido en el mensaje y envia los mensajes cada  0.08 segundos.
def canal(letraB):
  letraR,CausaR = ruido(letraB)
  # print(CausaR)
  # print(letraR)
  velocidad_mbps = 100
  tiempo_teórico = 8 / velocidad_mbps  # Convertimos megabits a bits
  time.sleep(tiempo_teórico)
  verdad = random.randint(0, 1)
  if(verdad):
    print("transferiendo")
  return letraR,CausaR

#Decodifica el mensaje de binario a carácter
def decodifica(letraB):
  #  bits a decimal
  decimal = int(letraB, 2)
  # decimal a carácter
  caracter = chr(decimal)
  return caracter

#Recibe el mensaje enpaquetado y lo decodifica de binario a caracter
def receptor(listaB):
  MensajeFin = []
  listaRuido = []
  # print(len(listaB)-2)
  if((listaB[0] == 'INI') & (listaB[len(listaB)-1] == 'FIN')):
    for i in range(1,len(listaB)-1):
      # print(listaB[i])
      BinR,CausaC = canal(listaB[i])
      #guardar probabilidades
      if(CausaC):
        listaRuido.append(1/(len(listaB)-2))
      else:
        listaRuido.append(0)

      Letra = decodifica(BinR)
      MensajeFin.append(Letra)
    print("lista de probabilidades: ",listaRuido)
    print("Entropia de shannon: ",EntropiaAleatoria(listaRuido))
  else:
    print("EL mensaje no se encuentra enpaquetado")

  return MensajeFin

#recibe la lista de caracteres y las pasa a un string
def Destino(Mensaje):
  MensajeDestino = ''.join(Mensaje)
  print("Mensaje Recibido... :",MensajeDestino)

# #Escribir mensaje
# mensaje = Finformacin()
# print("Mensaje enviado.... :",mensaje)

# #pasar el mensaje a una lista
# ListMensaje = separar(mensaje)

# #convertir cada uno de los caracteres a binario
# BinariList = [transmite(caracter) for caracter in ListMensaje]

# #enpaquetar los datos
# packBList = enpaquetar(BinariList)
# #recibir y decodificar los datos
# entrega = receptor(packBList)

# #recbir los datos finales y convertir de lista a string
# Destino(entrega)



"""# Aplicar Huffman

## arbol Huffman
"""

import copy # para objetos más complejos o personalizados

class Nodo:
    def __init__(self, dato, izquieda=None, derecho=None):
        self.dato = dato
        self.izquieda = izquieda
        self.derecho = derecho

class Arbol:
    # Funciones privadas
    def __init__(self, dato):
        self.raiz = Nodo(dato)

    def __inicializar_arbol(self,nodo,dato1,dato2):
      #Obtner raiz
      if isinstance(dato1, Nodo):
        # print(1)
        if dato1.dato <= dato2:
          self.__agregar_nodo_izquieda(nodo,dato2) #EL MENOR
          self.__agregar_nodo_derecho(nodo,dato1)
        else:
          self.__agregar_nodo_izquieda(nodo,dato1) #EL MENOR
          self.__agregar_nodo_derecho(nodo,dato2)

      if isinstance(dato2, Nodo):
        # print(2)
        if dato1 <= dato2.dato:
          self.__agregar_nodo_izquieda(nodo,dato2) #EL MENOR
          self.__agregar_nodo_derecho(nodo,dato1)
        else:
          self.__agregar_nodo_izquieda(nodo,dato1) #EL MENOR
          self.__agregar_nodo_derecho(nodo,dato2)

      if (not isinstance(dato1, Nodo)) & (not isinstance(dato1, Nodo)) :
        # print(3)
        if dato1 <= dato2:
          self.__agregar_nodo_izquieda(nodo,dato2) #EL MENOR
          self.__agregar_nodo_derecho(nodo,dato1)
        else:
          self.__agregar_nodo_izquieda(nodo,dato1) #EL MENOR
          self.__agregar_nodo_derecho(nodo,dato2)

    def __agregar_recursivo(self, nodo): #para shannon
        if len(nodo.dato) == 2:
          # print("lista",nodo.dato, "tamaño", len(nodo.dato))
          nodo.izquieda = Nodo([nodo.dato[0]])
          nodo.derecho = Nodo([nodo.dato[1]])


        elif len(nodo.dato) == 1:
          # print("lista",nodo.dato, "tamaño", len(nodo.dato))
          nodo.izquieda = Nodo([nodo.dato[0]])


        else:
          lista_separar = nodo.dato
          # print("lista completa",lista_separar, "tamaño", len(lista_separar))

          mitad = math.floor(len(lista_separar) /2) #redondear hacia abajo
          mitad1 = lista_separar[0:mitad]
          mitad2 = lista_separar[mitad:len(lista_separar)]
          # print("mitad1",mitad1)
          # print("mitad2",mitad2)
          nodo.izquieda = Nodo(mitad1)
          nodo.derecho = Nodo(mitad2)
          self.__agregar_recursivo(nodo.izquieda)
          self.__agregar_recursivo(nodo.derecho)

    def __buscar_shannon(self, nodo, busqueda,palabra=""):

        # print("inicia izquierda", nodo.izquieda.dato)

        if len(nodo.izquieda.dato) == 1:

          if nodo.izquieda.dato[0] == busqueda:
                return "0" + palabra

        # print("inicia derecho", nodo.derecho.dato)
        if len(nodo.derecho.dato) == 1:

          if nodo.derecho.dato[0] == busqueda:
                return "1" + palabra

        if busqueda in nodo.izquieda.dato:
          # print("entra izquierda",nodo.izquieda.dato )
          return self.__buscar_shannon(nodo.izquieda,busqueda,"0" + palabra)
        else:
          # print("entra derecha",nodo.derecho.dato )
          return self.__buscar_shannon(nodo.derecho,busqueda,"1" + palabra)

    def __agregar_nodo_derecho(self,nodo,dato1):
      if isinstance(dato1, Nodo):
        nodo.derecho = dato1
        # print("nodo_derecho")
      else:
        nodo.derecho = Nodo(dato1) #penultimo menor
        # print("numero_derecho")

    def __agregar_nodo_izquieda(self,nodo,dato1):
      if isinstance(dato1, Nodo):
        nodo.izquieda = dato1
        # print("nodo_izquierdo")
      else:
        nodo.izquieda = Nodo(dato1) #penultimo menor
        # print("numero_izquierdo")


    def __buscar(self, nodo, busqueda,palabra=""):

        if(nodo.izquieda.dato == busqueda) | (nodo.derecho.dato == busqueda):

          if(nodo.izquieda.dato == busqueda):
            # print(busqueda,"encontrado en izquierda")
            return "0" + palabra
          elif(nodo.derecho.dato == busqueda):
            # print(busqueda,"encontrado en derecho")
            return "1" + palabra
        else:

          if (nodo.derecho.izquieda is not None) | (nodo.derecho.derecho is not None) :

            return self.__buscar(nodo.derecho, busqueda, "1" + palabra)

          else:
            return self.__buscar(nodo.izquieda, busqueda,"0" + palabra)



    def __inorden_recursivo(self, nodo):
        if nodo is not None:
            self.__inorden_recursivo(nodo.izquieda)
            print(nodo.dato, end=", ")
            self.__inorden_recursivo(nodo.derecho)

    def __preorden_recursivo(self, nodo):
        if nodo is not None:
            print(nodo.dato, end=", ")
            # print(nodo.derecho.dato)
            self.__preorden_recursivo(nodo.izquieda)
            self.__preorden_recursivo(nodo.derecho)

    def __postorden_recursivo(self, nodo):
        if nodo is not None:
            self.__postorden_recursivo(nodo.izquieda)
            self.__postorden_recursivo(nodo.derecho)
            print(nodo.dato, end=", ")

    def inorden(self):
        print("Imprimiendo árbol inorden: ")
        self.__inorden_recursivo(self.raiz)
        print("")

    def preorden(self):
        print("Imprimiendo árbol preorden: ")
        self.__preorden_recursivo(self.raiz)
        print("")

    def postorden(self):
        print("Imprimiendo árbol postorden: ")
        self.__postorden_recursivo(self.raiz)
        print("")

    def agregar(self):
        self.__agregar_recursivo(self.raiz)

    def agregar_ini(self, dato1,dato2):
        self.__inicializar_arbol(self.raiz, dato1,dato2)

    def buscar(self, busqueda):
        return self.__buscar(self.raiz, busqueda)

    def buscar_shannon(self, busqueda):
        return self.__buscar_shannon(self.raiz, busqueda)

def arbol_huffman(lista_ordenada):
  ultimo = lista_ordenada[len(lista_ordenada)-1]
  penultimo = lista_ordenada[len(lista_ordenada)-2]

  raiz1 = ultimo + penultimo
  Huffman = Arbol(raiz1)
  Huffman.agregar_ini(ultimo,penultimo)
  Huffman_copia = copy.copy(Huffman)

  for i in reversed(range(0, len(lista_ordenada)-2)):

    if i != 0:
      raiz = lista_ordenada[i] + raiz1
      Huffman_principal = Arbol(raiz)
      Huffman_principal.agregar_ini(Huffman_copia.raiz,lista_ordenada[i])
      Huffman_copia = copy.copy(Huffman_principal)
    else:
      Huffman_principal = Arbol(None)
      Huffman_principal.agregar_ini(Huffman_copia.raiz,lista_ordenada[i])

  return Huffman_principal

# # lista = [.09,.4,0.5,.01]
# lista = [.5,.4,.3,.2,]
# lista_ordenada = sorted(lista, reverse=True)
# Huffman_principal = arbol_huffman(lista_ordenada)

# lista_Huffman = []
# for i in lista_ordenada:
#   lista_Huffman.append(Huffman_principal.buscar(i))
#   print(i," ",Huffman_principal.buscar(i))

"""##Esquema de comunicación con huffman"""

from collections import Counter

#obtener frecuencias relativas y ordenarlas de mayor a menor
def Obtener_frecuencias_relativas(lista_patrones):

  # Calcular la frecuencia de cada palabra
  contador = Counter(lista_patrones)
  # print(contador)
  # Calcular el número total de palabras en la lista
  total_palabras = len(lista_patrones)

  palabras = []
  frecuencias_relativas = []

  # Calcular la frecuencia relativa de cada palabra y agregarla a las listas
  for palabra, count in contador.items():
      palabras.append(palabra)
      frecuencia_relativa = count / total_palabras
      frecuencias_relativas.append(frecuencia_relativa)
  # Ordenar las palabras y frecuencias juntas en función de las frecuencias (de mayor a menor)
  palabras_ordenadas, frecuencias_ordenadas = zip(*sorted(zip(palabras, frecuencias_relativas), key=lambda x: x[1], reverse=True))

  # Convertir la tupla en una lista
  palabras_ordenadas = list(palabras_ordenadas)
  frecuencias_ordenadas = list(frecuencias_ordenadas)

  #hacer una diferencia para aquellos numero que sean iguales
  for i in range(0,len(frecuencias_ordenadas)-1):
    suma =1e-12
    for j in range(i,len(frecuencias_ordenadas)-1):
      if(frecuencias_ordenadas[i] == frecuencias_ordenadas[j+1]):
        # print(i," ", frecuencias_ordenadas[i]," ",j+1,frecuencias_ordenadas[j+1])
        frecuencias_ordenadas[j+1] = frecuencias_ordenadas[j+1] - suma
        # print(i," ", frecuencias_ordenadas[i]," ",j+1,frecuencias_ordenadas[j+1])
        suma = suma + 1e-12
      else:
        break;

  return palabras_ordenadas,frecuencias_ordenadas

#agarra la lista de bits y codifica a huffman
def Transmisor_huffman(BinariList):
  #obtner frecuencias y patrones ordenados
  patrones,frecuencias = Obtener_frecuencias_relativas(BinariList)
  Huffman = arbol_huffman(frecuencias)

  lista_Huffman = []
  for i in frecuencias:
    lista_Huffman.append(Huffman.buscar(i))
    # print(i," ",Huffman.buscar(i))
  return dict(zip(patrones, lista_Huffman))

#agarra la lista de bits y codifica a huffman
def Transmisor_shannon(BinariList):
  #obtner frecuencias y patrones ordenados
  patrones,frecuencias = Obtener_frecuencias_relativas(BinariList)
  Shannon = Arbol(frecuencias)
  Shannon.agregar()

  lista_Huffman = []
  for i in frecuencias:
    lista_Huffman.append(Shannon.buscar_shannon(i))
    # print(i," ",Huffman.buscar(i))
  return dict(zip(patrones, lista_Huffman))

def codificar_lista(BinariList,handshake):
  codificar = []
  for i in BinariList:
    codificar.append(handshake[i])
  return codificar

"""**El farsante - Ozuna**

Mi libertad no la quiero
Tampoco la vida de soltero
Yo lo que quiero es que quieras lo mismo que todos queremos
Tener una cuenta de banco con dígitos y muchos ceros
Hacer el amor a diario y de paso gastar el dinero
"""

#Escribir mensaje
# mensaje = Finformacin()
# print("Mensaje enviado.... :",mensaje)
mensaje = "Mi libertad no la quiero Tampoco la vida de soltero Yo lo que quiero es que quieras lo mismo que todos queremos Tener una cuenta de banco con dígitos y muchos ceros Hacer el amor a diario y de paso gastar el dinero"
print(" ")

#1 huffman
#0 shannon
verdad = 1

#pasar el mensaje a una lista
ListMensaje = separar(mensaje)

#convertir cada uno de los caracteres a binario
BinariList = [transmite(caracter) for caracter in ListMensaje]

#realizar reglas segun el agoritmo
if verdad:
  handshake_reglas = Transmisor_huffman(BinariList)
else:
  handshake_reglas = Transmisor_shannon(BinariList)


#agarrar cada paquete y codificarlo
codificar =  codificar_lista(BinariList,handshake_reglas)
print(codificar)


# #enpaquetar los datos
# packBList = enpaquetar(BinariList)
# #recibir y decodificar los datos
# entrega = receptor(packBList)

# #recbir los datos finales y convertir de lista a string
# Destino(entrega)