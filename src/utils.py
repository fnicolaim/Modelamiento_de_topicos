__author__ = ['Francisco Nicolai']
__email__ = ['f.n.manaut@gmail.com']
__status__ = 'Prototype'


"""
Utils for running Entel's call center semi-automatization model
"""

import pandas as pd

def pp_carga(carga):
    """
    Takes a loaded list of lists and return a pandas dataframe version of the same 
    with accomodation of headers and indexes.
    :param carga: List of lists 
    :type: list (n_samples +1)
    :return: Pandas DataFrame
    :type: object
    """
    df = pd.DataFrame(carga)  
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    df = df.reset_index(drop=True);
    return df


def filtro_probs(prediccion,p_min):
    """
    Takes a list of lists (2 elements each of the inner ones) and returns the same list
    with its innter contents filtered, only keeping the ones whose 2nd element is bigger
    than pmin.
    :param prediccion: List of lists 
    :type: list (n_predicted classes by lda)
    :param: pmin
    :type: float (min_value required to pass filter)
    :return: List of lists
    :type: List
    """
    clases = []
    for probabilidad in prediccion:
        if probabilidad[1]>=p_min:
            clases.append(probabilidad)
        else:
            clases.append("-")
    return clases

def add_tags(df,lda,corpus,pmin):
    """
    Takes a dataframe and adds the 3-top tags associated with the LDA model prediction over
    a corpus of interest.
    :param DF: Pandas DataFrame 
    :type: Object (n_samples x n_features)
    :param lda: Latent Dirichlet Allocation model
    :type: Gensim model
    :param corpus: Corpus of interest (BoW format)
    :type: List of tuples
    :param: pmin
    :type: float (min_value required to pass filter)
    :return: Pandas DataFrame with added columns
    :type: Object 
    """
    vector =[]
    for doc in corpus:
        prediccion = lda[doc]
        prediccion.sort(reverse= True,key=lambda x: x[1])
        prediccion = (filtro_probs(prediccion,pmin))
        vector.append(prediccion)
	    
    M1_glob = [item[0] for item in vector]
    M1_final = [item[0] for item in M1_glob]
    M2_glob = [item[1] for item in vector]
    M2_final = [item[0] for item in M2_glob]
    M3_glob = [item[2] for item in vector]
    M3_final = [item[0] for item in M3_glob]

    df["Pred_M1"] = M1_final
    df["Pred_M2"] = M2_final
    df["Pred_M3"] = M3_final

    return df


import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
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
