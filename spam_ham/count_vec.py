import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

df=pd.read_csv("new_df_spam.csv")
stop_words = set(stopwords.words('english')) 
cVect = CountVectorizer()
X = df.loc[:, 'text']
y = df.loc[:, 'class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=11)
cVect.fit(X_train)
def prediction(text):
    
    text = [' '.join([ word for word in word_tokenize(text)  if not word in stop_words])]
        # cVect.fit(text)
    t_dtv = cVect.transform(text).toarray()
    return t_dtv
     
