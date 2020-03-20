#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# General
import pandas as pd
import numpy as np
from IPython.display import display

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

#Propias
import metricas
import bautizo_prepago as bt
import config_bt_prepago as cf
l_gral_lema_stem = cf.l_gral_lema_stem_v6

#prediccion_conjunto_test
#  modelo_lda = lda
#  diccionario = dictionary
#  df_test= test_etiquetado
#  pmin = prob minima para realizacion prediccion
#  modo = 0 o 1 para usar como clasificador o vector de caracteristicas
def prediccion_conjunto_test(modelo_lda, diccionario, df_test, pmin=0.35, modo=0,verbose=False):
    ### "Bautizo topicos" ###
    probabilidades_topicos=[]                                                                           
    palabras_topicos=[]                                                                                 
    n_topicos = len(modelo_lda.get_topics())
    
    for topico in modelo_lda.show_topics(num_topics = n_topicos, num_words=10,log=False, formatted=True):         
        palabras_topicos.append((bt.recuperacion_palabras_topicos(topico[1]),topico[0]))                
        probabilidades_topicos.append((bt.recuperacion_probabilidades_marginales(topico[1]),topico[0])) 
    diccionario_exterior = bt.creacion_lut_temas(probabilidades_topicos,palabras_topicos)               
    
    if modo == 0 and verbose:    
        display(diccionario_exterior)                                          

    #Creacion diccionario tema-nombre
    ponderaciones_globales = bt.bautizo_topicos_ponderado(diccionario_exterior,l_gral_lema_stem)        
    if modo == 0 and verbose:
        print(ponderaciones_globales)                                                                   
    dicc_temas = dict(bt.bautizo_final(ponderaciones_globales,cf.D_d_D[n_topicos]))
    
    ### Predicción ###
    corpus_train_test = list(df_test["Descripción"])
    corpus_train_test = [diccionario.doc2bow(text) for text in corpus_train_test]
    
    if modo == 0:
        vector =[]
        for doc_nuevo in corpus_train_test:                                                                 
            prediccion = modelo_lda[doc_nuevo]                                                              
            prediccion.sort(reverse= True,key=lambda x: x[1])                                               
            prediccion = (metricas.filtro_probs(prediccion,pmin))                                           
            vector.append(prediccion)                                                                       

        #Asignación clasificaciones
        Pred_M1 = pd.Series([item[0][0] for item in vector])
        Pred_M2 = pd.Series([item[1][0] for item in vector])
        Pred_M3 = pd.Series([item[2][0] for item in vector])

        df = pd.concat([Pred_M1, Pred_M2, Pred_M3], axis=1)
        df.columns = ["Pred_M1","Pred_M2","Pred_M3"]

        #Traducción clasificación numérica a tema legibles
        for k,_ in enumerate(dicc_temas):
            df = df.replace(k,dicc_temas[k])
        
    if modo == 1:
        vector =[]
        for doc_nuevo in corpus_train_test:
            prediccion = modelo_lda[doc_nuevo]
            vector.append(prediccion)

        valores = [topico[1] for doc in vector for topico in doc]
        valores = np.reshape(valores, (-1, len(prediccion)))
        
        columnas = np.linspace(0,len(prediccion)-1,len(prediccion)).astype(int)
        
        df = pd.DataFrame(valores,columns=columnas)
        df = df.rename(columns = dicc_temas)
        
    return df 