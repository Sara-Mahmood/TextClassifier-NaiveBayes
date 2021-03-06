# -*- coding: utf-8 -*-
"""Interview-Task.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jAcmN9itTv66qv_ogqFVgxRsqMvtW9aD
"""

from sklearn.metrics import f1_score

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from urllib.request import urlopen
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import re
import nltk

!pip install clean-text

from cleantext import clean as clean_text

from sklearn.neighbors import KNeighborsClassifier

def parser(url):
  source = urlopen(url).read()
  soup = BeautifulSoup(source, "lxml")
  paragraphs = soup.find_all('p')
  text = ""

  for p in paragraphs:
      text += p.text
  return text

nltk.download("punkt")

df = pd.DataFrame(columns = ["Text", "label"])
urls_tech = ["https://techcrunch.com/2020/05/04/tumblr-now-removes-reblogs-in-violation-of-its-hate-speech-policy-not-just-the-original-posts/", "https://techcrunch.com/2019/11/18/pitch-on-stage-at-techcrunchs-robotics-ai-show-march-3-at-ucberkeley/",
             "https://techcrunch.com/2019/10/15/product-lessons-from-building-our-subscription-service-extra-crunch/", "https://techcrunch.com/2019/07/23/almost-sold-out-buy-a-ticket-to-the-14th-annual-techcrunch-summer-party/",
             "https://en.wikipedia.org/wiki/Machine_learning", "https://en.wikipedia.org/wiki/Artificial_intelligence"]

for url in urls_tech:
  text = parser(url)
  text = clean_text(text)
  all_sentences = nltk.sent_tokenize(text)
  for s in all_sentences:
    df.loc[len(df)] = [s , "tech"]

print(df)

urls_weather = [ "https://en.wikipedia.org/wiki/Atmosphere", "https://en.wikipedia.org/wiki/Temperature", "https://en.wikipedia.org/wiki/Thermal_energy",
                "https://en.wikipedia.org/wiki/Climate_variability_and_change", "https://en.wikipedia.org/wiki/Atlantic_multidecadal_oscillation", "https://en.wikipedia.org/wiki/Glossary_of_meteorology"]


for url in urls_weather:
  text = parser(url)
  text = clean_text(text)
  all_sentences = nltk.sent_tokenize(text)
  for s in all_sentences:
    df.loc[len(df)] = [s , "weather"]

print(df)

urls_politics = [ "https://www.latimes.com/politics/story/2021-02-07/joe-biden-had-a-choice-go-big-or-go-bipartisan-he-opted-for-big", "https://edition.cnn.com/2021/02/07/politics/biden-republican-opposition/index.html", 
                 "https://www.aljazeera.com/news/2020/11/19/pakistan-pm-khan-headed-for-his-maiden-afghan-visit"]

for url in urls_politics:
  text = parser(url)
  text = clean_text(text)
  all_sentences = nltk.sent_tokenize(text)
  for s in all_sentences:
    df.loc[len(df)] = [s , "politics"]

df

def clean_text(text):
    text = text.lower()
    text = re.sub(r"@[A-Za-z0-9]+", ' ', text)
    text = re.sub(r"https?://[A-Za-z0-9./]+", ' ', text)
    text = re.sub(r"[^a-zA-z.!?'0-9]", ' ', text)
    text = re.sub('\t', ' ',  text)
    text = re.sub(r" +", ' ', text)
    return text

def preprocess(X, y):
  le = preprocessing.LabelEncoder()
  Y = le.fit_transform(y)
  vectorizer = CountVectorizer()
  vectorizer.fit(X)
  X = vectorizer.transform(X)
  return X, y, vectorizer

def train(X_train , y_train):
  neigh = GaussianNB()
  neigh.fit(X_train, y_train)
  return neigh

def predict(X_test,y_true, model):
  result = model.predict(X_test)
  print("The accuracy of the given model is: ", accuracy_score(y_true, result))
  print("F1 score is:", f1_score(y_true, result, average='macro'))
  return result

X= df['Text']
y = df['label']
X, y, preprocess_model = preprocess(X, y)
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.33, random_state=42)
model = train(X_train.toarray(), y_train)
result = predict(X_test.toarray(), y_test, model)

def make_prediction(text, model, preprocess_model):
  text = [text]
  text = clean_text(str(text))
  text = [text]
  X = preprocess_model.transform(text)
  X = X.toarray()
  return model.predict(X)

input_text = input()
print(make_prediction(input_text, model, preprocess_model))

"""suggestions for improvement:

There are several other approaches that could be tried out 

1. using doc2vec or word2vec for preprocessing, this would help take make embeddings and extract semantic features from the text.
2.  the corpus used could be made better through scraping the articles from various diverse sources.
3. the number of articles scraped could be increased.
4. ML techniques do give good results for text classification but CNN and other DL techniques could also be used. using DL would go in more depth and extract and would  learn better. This approach would have been better with larger corpus.
5. pretrained models like XLNet could also be used for transfer learning to fit to this taks. XLNet gives almost 98% accuracy for the sentimentAnalysis task which is a classification task itself, that model could be used and extend to make 3 class classification.

"""