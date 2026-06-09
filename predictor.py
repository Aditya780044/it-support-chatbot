```python
import pickle
import pandas as pd
import re
import nltk

# Download NLTK data if not available
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load model
with open('models/chatbot_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load data files
df = pd.read_excel('data/knowledge_base.xlsx')
sop_df = pd.read_excel('data/sop_mapping.xlsx')

# NLP setup
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return ' '.join(words)

def get_response(user_query):
    cleaned = clean_text(user_query)
    category = model.predict([cleaned])[0]

    matches = df[df['category'] == category]

    if len(matches) == 0:
        return category, 'Please contact IT Helpdesk.', [], ''

    answer = matches.iloc[0]['answer']
    steps_raw = matches.iloc[0]['steps']

    steps = [
        s.strip()
        for s in str(steps_raw).split('.')
        if s.strip()
    ]

    sop_match = sop_df[sop_df['category'] == category]

    sop_file = (
        sop_match.iloc[0]['sop_filename']
        if len(sop_match) > 0
        else ''
    )

    return category, answer, steps, sop_file
```
