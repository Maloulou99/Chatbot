import nltk
import string
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from enchant.checker import SpellChecker
from nltk.corpus import stopwords

# Ensure necessary nltk data is downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize stop words
stop_words = set(stopwords.words('english'))

# Function to preprocess input text
def preprocess_input(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in string.punctuation]
    return tokens

# Function to stem tokens
def stem(tokens):
    lancaster = LancasterStemmer()
    stemmed_tokens = [lancaster.stem(token) for token in tokens]
    return stemmed_tokens

# Function to lemmatize tokens
def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

# Function to filter out stop words
def filter_for_stop_words(tokens, stop_words):
    return [word for word in tokens if word not in stop_words]

# Function to correct spelling errors
def correct_spelling(text):
    checker = SpellChecker("en_US")
    checker.set_text(text)
    for err in checker:
        suggestions = err.suggest()
        if suggestions:
            err.replace(suggestions[0])
    corrected_text = checker.get_text()
    return corrected_text
