import pandas as pd
import nltk
import pickle
import os
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline

df = pd.read_excel('data/knowledge_base.xlsx')
print(f'Loaded {len(df)} rows')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return ' '.join(words)

df['clean_query'] = df['query'].apply(clean_text)
print('Text cleaning done')

X = df['clean_query']
y = df['category']

model = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1,2))),
    ('clf', LinearSVC())
])

model.fit(X, y)
print('Model trained')

scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f'Accuracy: {scores.mean()*100:.1f}%')

os.makedirs('models', exist_ok=True)
with open('models/chatbot_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print('Done! Model saved.')