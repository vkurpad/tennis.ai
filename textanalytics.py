#from azureml.dataprep import package
#from azureml.logging import get_azureml_logger
import pandas as pd
import re
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.metrics import classification_report, confusion_matrix
#logger = get_azureml_logger()

# TODO: read in data
# script assumes data is in a df with two columns: label and filecontent

df = pd.read_csv("", )


def cleantext(raw_text):
    raw_text = bytes(raw_text, "utf-8").decode("unicode_escape")
    cleanr = re.compile('<.*?>')
    out = re.sub(cleanr, '', raw_text)
    out = re.sub("\n", "", out)
    out = re.sub("\r", "", out)
    out = re.sub("\t", "", out)
    out = re.sub("&#160;", "", out)
    out = out.replace('3 ', 'three')
    out = out.replace('12 ', 'twelve')
    out = re.sub('[^A-Za-z0-9 /.]+', ' ', out)
    #out = re.sub('[^A-Za-z]+', ' ', out)
    out = out.strip().lower()
    return out

# Using cleantext function to clean text column
df['filecontent'] = list(map(cleantext, df['filecontent']))

# Splitting data into train/test
X = df['filecontent']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
print("Data Processed")

# Creating pipeline
pipeline = Pipeline([
    ('vect', CountVectorizer(stop_words = 'english', ngram_range= (1, 2))),
    ('tfidf', TfidfTransformer()),
    ('bc', BaggingClassifier(n_estimators=20))
])

# Fitting pipeline
pipeline.fit(X_train, y_train)
print("Finished Training Model")


## save the model to file
import pickle
s = pickle.dumps(pipeline)


## load the model
pipeline = pickle.loads(s)


# Scoring model and outputting results
pred = pipeline.predict(X_test)
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))