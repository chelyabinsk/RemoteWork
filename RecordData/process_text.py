# -*- coding: utf-8 -*-
"""
Process the comments into usable format
"""

# download stopwords corpus, you need to run it once
import nltk
import pandas as pd
nltk.download("stopwords")
#--------#

from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
import re

#from sklearn.model_selection import train_test_split

#Create lemmatizer and stopwords list
mystem = Mystem() 
russian_stopwords = stopwords.words("russian")

#Preprocess function
def preprocess_text(text):
    try:
        tokens = mystem.lemmatize(text.lower())
    except AttributeError:
        return text        
    tokens = [token for token in tokens if token not in russian_stopwords\
              and token != " " \
              and token.strip() not in punctuation]
    
    text = " ".join(tokens)
    r = re.compile("[а-яА-Я\s]+")
    text = " ".join(re.findall(r, text))
#    text = [w for w in filter(r.match, text)]
    
    return text

def clean_data(fn):

    ## Load data
    print('loading data')
    df = pd.read_csv('comments/{}.txt'.format(fn),sep='\t')
#    nrows = model_data.shape[0]
#    
#    msgs = model_data['message']
#    channels = model_data['channel']
#    full = pd.DataFrame({"channel":[],"clean":[]})
#    for i in range(nrows):
#        tmp = pd.DataFrame({"channel":[channels[i]],"clean":[preprocess_text(msgs[i])]})
#        full = full.append(tmp)
#        print(i,nrows,round(i/nrows*100,2))
    df['clean'] = df['message'].apply(preprocess_text)
    df.to_csv('comments/c_{}.txt'.format(fn),sep='\t')
    
#clean_data('2020-09-15')
#clean_data('2020-09-17')
#clean_data('2020-09-23')
#clean_data('2020-09-24')
#clean_data('2020-09-25')
#clean_data('2020-09-26')
#clean_data('2020-09-27')
