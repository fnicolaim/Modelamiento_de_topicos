import re
import numpy as np
from operator import itemgetter

#Estas funciones se añaden para trabajar sobre output de gensim LDA
def recuperacion_probabilidades_marginales(text):
    text = re.sub(r'[^0-9.\s]+', '', text)
    tokens = text.split()  #El string es transformado a una lista, el separador por defecto es un espacio
    tokens = [i.lower() for i in tokens]        # Todo a minúsculas    
    tokens = text.split()  #El string es transformado a una lista, el separador por defecto es un espaci
    return tokens

def recuperacion_palabras_topicos(text):
    text = re.sub(r'\n', '', text) #elimina símbolo de salto de línea
    text = re.sub(r'\.', ' ', text) #reemplazamos los puntos por un espacio
    text = re.sub(r'[^\w\s]','', text) #elimina los símbolos de puntuación
    text = re.sub(r'[a-zA-Z]+[0-9]+', '', text) #elimina los caracteres que contienen letras y números
    text = re.sub(r'[0-9]+', ' ', text) #elimina los caracteres numéricos
    tokens = text.split()  #El string es transformado a una lista, el separador por defecto es un espacio
    tokens = [i.lower() for i in tokens]        # Todo a minúsculas    
    return tokens

def creacion_lut_temas(probabilidades_topicos,palabras_topicos):
    tupla_exterior=[]
    for i in range(len(palabras_topicos)):
        topico = palabras_topicos[i]
        llave_exterior = topico[1]
        tupla_interior=[]
        for j in range(len(topico[0])):
            llave_interior = topico[0][j]
            valor_interior = probabilidades_topicos[i][0][j]
            tupla_interior.append((llave_interior,valor_interior))
        diccionario_interior = dict(tupla_interior)
        valor_exterior = diccionario_interior
        tupla_exterior.append((llave_exterior,valor_exterior))
    diccionario_exterior = dict(tupla_exterior)
    return diccionario_exterior

def bautizo_topicos_ponderado(diccionario_exterior,lista_gral):
    ponderaciones_globales= []
    for tema in diccionario_exterior.keys():                                # Para cada uno de los 4 subdiccionarios....
        ponderaciones_topico = []
        for tema_lista in lista_gral:                                       # Para cada uno de los 4 temas predefinidos
            palabras_comun = list(set(diccionario_exterior[tema].keys()) & set(tema_lista[1]))
            ponderadores = [float(diccionario_exterior[tema][palabra]) for palabra in palabras_comun]
            suma_clase = (round(sum(ponderadores),3),tema_lista[0])
            ponderaciones_topico.append(suma_clase)    
        ponderaciones_globales.append(ponderaciones_topico)
    return ponderaciones_globales

def bautizo_final(ponderaciones_globales, predefined_dicc, verbose=False):
    resultado_final = []
    indices_mal_asignados = []
    for i,topico in enumerate(ponderaciones_globales):                     # Contador // a cada uno de los elementos en pond_glb
        #Excepción para cuando no hay ninguna palabra común entre clases y topicos modelos.
        if (max(topico,key=itemgetter(0))[0]) == 0:
            print("Se asignó tema ",i, "teniendo prob_marg acumulada 0, posible problema.\n")
            indices_mal_asignados.append(i)
            resultado_final.append((i,"No se asigna clase"))
        else:
            resultado_final.append((i,max(topico,key=itemgetter(0))[1]))
    if verbose:
        print(resultado_final,"\n\n")
    
    dif = set(predefined_dicc.keys()) - set(dict(resultado_final).values())
    if verbose:
        print("Clases no asignadas: ",dif, "\n")
    if len(dif) == 1:
        try:
            del resultado_final[indices_mal_asignados[0]]
            resultado_final.append((indices_mal_asignados[0],list(dif)[0]))#Los [0] se usan para retornar el valor en sí, sin los []
        except:
            print("No se asigno ",dif, "puesto que una clase se repitió. \n")
        if verbose:
            print(resultado_final)
            print("\n")
           
    return resultado_final
