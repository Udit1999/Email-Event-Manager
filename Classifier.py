import numpy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB




data = pd.DataFrame.from_csv('sample.csv')

vectorizer = CountVectorizer()
counts = vectorizer.fit_transform(data['Snippets'].values)
classifier = MultinomialNB()
targets = data['class'].values
classifier.fit(counts, targets)

examples = pd.read_csv('Inbox.csv')
example_counts = vectorizer.transform(examples['Snippets'])
predictions = classifier.predict(example_counts)
print(counts)
