import nltk
import string
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import enchant
from nltk.corpus import stopwords
import re

# Ensure necessary nltk data is downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize stop words
stop_words = set(stopwords.words('english'))

# Initialize the English dictionary for spell checking
spell_checker = enchant.Dict("en_US")

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

# Function to preprocess input text
def preprocess_input(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in string.punctuation]
    return tokens

def preprocess_input_chat(input_text):
    tokens = nltk.word_tokenize(input_text)

    tokens_lower = [token.lower() for token in tokens]
    
    return tokens_lower

def contains_yes_or_no(input_text):
    input_text = input_text.lower()
    yes_responses = ['yes', 'yah', 'yeah', 'yup', 'yep', 'sure', 'ok', 'okay', 'alright', 'definitely', 'absolutely']
    no_responses = ['no', 'nah', 'nope', 'not', 'never']
    
    if any(word in input_text for word in yes_responses):
        return 'yes'
    elif any(word in input_text for word in no_responses):
        return 'no'
    else:
        return None

# Function to count matched columns from the user input
def count_matched_tokens(user_tokens, recipe_tokens):
    set1 = set(user_tokens)
    set2 = set(recipe_tokens)

    total_matches = len(set1.intersection(set2))

    return total_matches

def extract_num_persons(input_text):
    match = re.search(r'\b(\d+)\b', input_text)
    return int(match.group(1)) if match else 1




