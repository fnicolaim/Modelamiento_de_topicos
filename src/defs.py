#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import nltk
import csv
import collections
import operator
import unicodedata

import os
cwd = os.getcwd()
root = os.path.dirname(cwd)
lematizador_dir = os.path.join(root,"data","lematizador","lematizador.csv")
stopwords_dir = os.path.join(root,"data","stopwords")

from spellchecker import SpellChecker #https://pypi.org/project/pyspellchecker/

#Stemmer
from nltk.stem.snowball import SpanishStemmer
stemmer = SpanishStemmer()

#Creación objeto para corrección ortografía
spell = SpellChecker(language="es")
metodo_desconocidas = spell.unknown
metodo_correccion = spell.correction 
lista_blanca_regiones = ["Arica", "Parinacota","Tarapacá","Antofagasta","Atacama","Coquimbo","Valparaíso","Metropolitana", "Santiago","Libertador",
                         "General", "Bernardo","O’Higgins","Maule","Ñuble","Biobío","Araucanía","Ríos","Lagos","Aysén", "General", "Carlos", "Ibáñez",
                         "Campo", "Magallanes", "Antártica"]
lista_blanca_telecom = ['lte','whatsapp','instagram','telegram','youtube','facebook','entel','bafi','resetea','samsung','huawei','iphone',
                                  'kb','mb','pixi','alcatel','movistar','wom','android','tv','rrss','anita','carlitos']
lista_blanca_telecom.extend(lista_blanca_regiones)
lista_blanca = lista_blanca_telecom
spell.word_frequency.load_words(lista_blanca)

#Stopwords
with open(os.path.join(stopwords_dir,"stopwords_1.csv"), 'r', encoding="utf8") as f:
  reader = csv.reader(f)
  stopwords_1 = list(reader)
with open(os.path.join(stopwords_dir,"stopwords_2.csv"), 'r', encoding="utf8") as f:
  reader = csv.reader(f)
  stopwords_2 = list(reader)
stopwords_1 = [item for sublist in stopwords_1 for item in sublist]
stopwords_2 = [item for sublist in stopwords_2 for item in sublist]
print("Cantidad de palabras lista stopwords nombres y técnicas:",len(stopwords_1))
print("Cantidad de palabras lista stopwords lingüistica:",len(stopwords_2))
stopwords_1.extend(stopwords_2)
s_w = stopwords_1.copy() #Cambiar a stopwords_1 si se quiere implementar ambas
print("Cantidad de palabras lista stopwords global:",len(s_w))


#Lematizador
with open(lematizador_dir, 'r', encoding="utf8") as f:
  reader = csv.reader(f)
  dic_lema = list(reader)
del dic_lema[0]
diccionario_lematizador = dict(dic_lema)
def lematizar(palabra, dic=diccionario_lematizador):
    try:
        palabra = dic[palabra]
    except:
        palabra = palabra
    return palabra
                 
def replace_all(text, dic): #https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def procesamiento_texto(text, stop_list=s_w, lema=False, stemming=False, stopword=True, ortografia=False, tildes=False):
    text=str(text)
    #Quitar caracteres no alfa numéricos    
    text = re.sub(r'\n', '', text)              #elimina símbolo de salto de línea
    text = text.replace('se?al','señal')        #reemplaza signos de interrogación por símbolo de salto de línea
    text = re.sub(r"\b%s\b" % "liente" , "cliente", text)
    text = re.sub(r"\b%s\b" % "iente" , "cliente", text)
    text = re.sub(r'\.', ' ', text)             #reemplaza puntos por un espacio
    text = re.sub(r'\,', ' ', text)             #reemplaza comas por un espacio
    text = re.sub(r'[^\w\s]','', text)          #elimina los símbolos de puntuación
    text = re.sub(r'[0-9]+', ' ', text)         #elimina los caracteres numéricos

    tokens = text.split()                       #El string es transformado a lista, separador por defecto es un espacio
    tokens = [i.lower() for i in tokens]        # Todo a minúsculas
    tokens = [i for i in tokens if len(i) > 1 and len(i)<15]  #Eliminar tokens con menos de 2 elementos y mas de 14

    #Stopwords
    if stopword == True:
        tokens = [i for i in tokens if i not in stop_list]

    #Ortografía
    if ortografia == True:
        espacio = ' '
        text = espacio.join(tokens)
        ##text = untokenize(tokens)
        misspelled = metodo_desconocidas(tokens)# Se identifica aquellas palabras mal escritas
        erradas_lista = list(misspelled)        # Redefine variable en clase de interés (serán llaves)

        correcciones = []
        for word in misspelled:
            correcciones.append(metodo_correccion(word))

        diccionario = dict(zip(erradas_lista, correcciones))
        text = replace_all(text,diccionario)

        tokens = text.split()                          ##El string a lista, separador por defecto es un espacio

        if stopword == True:
            tokens = [i for i in tokens if i not in stop_list]  # Nuevamente se remueven stopwords (caso de que algo se corrigiera a una)

    #Lematización, MUY Sensible a ortografía
    if lema == True:
        aux = []
        for palabra in tokens:
            aux.append(lematizar(palabra))
        tokens = aux

    #Stemming
    if stemming==True:    
        tokens = [stemmer.stem(w) for w in tokens]

    #Tildes
    if tildes==True:
        espacio = ' '
        text = espacio.join(tokens)
        text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore') #elimina todas marcas de acentuación
        text = text.decode("utf-8")             #Devuelve salida linea anterior a formato compatible
        tokens = text.split() 

    return tokens