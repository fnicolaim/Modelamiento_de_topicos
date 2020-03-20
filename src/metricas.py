#!/usr/bin/env python
# coding: utf-8

# General
import pandas as pd
import numpy as np
import time
from operator import itemgetter

#Matriz de confusión
import itertools
import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

#Remoción de NaNs en columna de clasificacion edo y modelo
def limpieza_reemplazo(df,reemplazo = True):
    df.dropna(subset=['M1'],inplace=True)
    df.dropna(subset=['Pred_M1'],inplace=True)
    df = df[df['Pred_M1'] != '-']
    if reemplazo==True:
        df = df.drop(df[df.M1 == "Pendiente"].index)
        df = df.replace("Bolsas y recargas",str("Otros"))
        df = df.replace("Canales",str("Otros"))
        df = df.replace("Requerimiento",str("Otros"))
        df = df.replace("Consulta",str("Otros"))
    return df

#Evaluación modelo retorna vector de probabilidades pertenencia para cada clase, se filtran aquellas con probabilidad < p_min
def filtro_probs(prediccion,p_min):
    clases = []
    for probabilidad in prediccion:
        if probabilidad[1]>=p_min:
            clases.append(probabilidad)
        else:
            clases.append("-")
    return clases

#Matriz de confusión
def plot_confusion_matrix(cm, classes,normalize=False,title='Confusion matrix',cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

#Accuracy top-3 (M1/pred1,2,3)
def revision_prediccion(top_clasificacion_real,pred1,pred2,pred3):
    i=0
    if top_clasificacion_real == pred1:
        i+=1
    else:
        if top_clasificacion_real == pred2:
            i+=1
        else:
            if top_clasificacion_real == pred3:
                i+=1
    return i

#"Accuracy" top-3v3 (M1,2,3/pred1,2,3)
def desempeño_especifico(df,target,verbose=False):
    pd.options.mode.chained_assignment = None
    
    df_aux = df.loc[( (df['M1'] == str(target) ) | (df['M2'] == str(target) ) | (df['M3'] == str(target) ) )]
    
    df_aux["Top"] = str(target)
    
    num_muestras = len(df_aux)
    aciertos = 0
    for index, row in df_aux.iterrows():
        aciertos += revision_prediccion(df_aux["Top"][index],df_aux["Pred_M1"][index],
                                       df_aux["Pred_M2"][index],df_aux["Pred_M3"][index])
    if verbose:
        print(f"Accuracy modelo (Top-3) en", str(target),f": {round(aciertos*100/len(df_aux),4)}%")
    resultados=(aciertos,len(df_aux),str(target))
    return resultados

# Se divide en dos casos, 2 etiquetas originales y una etiqueta original
def nueva_metrica_2v2(df):
	df = df.drop(["M3", "Pred_M3"], axis=1)
	total_2 = len(df)*2
	conteo = 0
	for index, fila in df.iterrows():
	    conteo_loc = 0
	    # Solo una etiqueta:
	    if not(fila["M2"] in df.M1.unique()):
	        if (fila["M1"] == fila["Pred_M1"]) or (fila["M1"] == fila["Pred_M2"]):
	            conteo_loc += 2
	    #2 etiquetas
	    else:    
	        if (fila["M1"] == fila["Pred_M1"]) or (fila["M1"] == fila["Pred_M2"]):
	            conteo_loc += 1
	        if (fila["M2"] == fila["Pred_M1"]) or (fila["M2"] == fila["Pred_M2"]):
	            conteo_loc += 1

	    conteo += conteo_loc

	metrica_nueva = round(conteo/total_2,5)
	return metrica_nueva