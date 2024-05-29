import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

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
    tokens = [token for token in tokens if token not in stop_words]
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
def filter_for_stop_words(tokens):
    return [word for word in tokens if word not in stop_words]

# Function to count matched tokens between user input and recipe
def count_matched_tokens(user_tokens, recipe_tokens):
    set1 = set(user_tokens)
    set2 = set(recipe_tokens)
    total_matches = len(set1.intersection(set2))
    return total_matches
