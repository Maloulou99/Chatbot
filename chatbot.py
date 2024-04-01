import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initializations and downloads
stop_words = set(stopwords.words('english'))

# Function to preprocess user input
def preprocess_input(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in string.punctuation]
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

#Recognize the shortcuts of a word
def stem(tokens):
 lancaster = LancasterStemmer()
 lancasterstemmed_tokens = [lancaster.stem(token) for token in tokens]
 return lancasterstemmed_tokens

#Recognize the root words
def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

#Deleting the words we dont have in keywords
stop_words = stopwords.words('english')
def filter_for_stop_words(tokens, stop_words):
    filtered = []
    for word in tokens:
        if word not in stop_words:
            filtered.append(word)
    return filtered

# Function to count matched colums from the userinput
def count_matched_tokens(user_tokens, recipe_tokens):
    set1 = set(user_tokens)
    set2 = set(recipe_tokens)

    total_matches = len(set1.intersection(set2))

    return total_matches

# Give the Chatbot a chance to send a new recipe to the same userinput
def get_matching_recipes(user_input, data): 
    user_tokens = preprocess_input(user_input)
    matching_recipes = []

    for recipe in data:
        match_counter = 0
        for key, value in recipe.items():
            if key in ['DishName', 'Step']:
                continue  
            if isinstance(value, str):
                recipe_tokens = preprocess_input(value)
                match_counter += count_matched_tokens(user_tokens, recipe_tokens)

        matching_recipes.append((recipe, match_counter))

    if matching_recipes:
        max_match_count = max(matching_recipes, key=lambda x: x[1])[1]
        top_matching_recipes = [recipe[0] for recipe in matching_recipes if recipe[1] == max_match_count]

        return top_matching_recipes

current_recipe_index = 0
repeated_recipe = False

# Main Chatbot chat
def chat():
    global current_recipe_index, repeated_recipe
    print("Hello, I hope you are doing well! Welcome to your personal Recipe Finder!")
    print("You can tell me which ingredients or categories you have, and I can provide you with recipes based on those.")
    print("So let's start, what ingredients or categories do you have?")
    print("Please write 'exit' when you are finished!")

    df = pd.read_csv('csv/recipe.csv')
    data = df.to_dict(orient='records')

    all_words = list(set(df['Keywords'].str.lower().str.split().sum()))
    processed_all_words = stem(all_words)
    processed_all_words = lemmatize(processed_all_words)

    #categories = list(set(df['Category'].str.lower()))

    conversation = [] 
    prev_output = None

    while True:
        user_input = input("You: ").lower() 

        if user_input == 'exit':
            print("Thank you, enjoy your meal! Goodbye and I hope to see you soon!")
            break

        if prev_output != user_input:
            print("DishDive:", end=" ")
        
        conversation.append(user_input) 

        processed_input = preprocess_input(user_input)
        processed_input = filter_for_stop_words(processed_input, stop_words)
        processed_input = stem(processed_input)
        processed_input = lemmatize(processed_input)
        #processed_input = find_keywords_and_category(processed_input, processed_all_words, categories)
        matching_recipes = get_matching_recipes(user_input, data)  

        if matching_recipes:
            if current_recipe_index < len(matching_recipes):
                print("Based on your ingredients or categories, here is a recipe recommendation:")
                print(matching_recipes[current_recipe_index]['DishName'])
                print(matching_recipes[current_recipe_index]['Step'])
                conversation.append(matching_recipes[current_recipe_index]['Step'])
                current_recipe_index += 1 
            else:
                print("I have sent you all the recipes I have with your ingredients or categories.")
                repeat_response = input("Would you like to see a recipe again?\nYou: ").lower()
                if repeat_response == 'yes':
                    current_recipe_index = 0  
                    print("Here is the first recipe recommendation again:")
                    print(matching_recipes[current_recipe_index]['Step'])
                    conversation.append(matching_recipes[current_recipe_index]['Step'])
                    current_recipe_index += 1  
                else:
                    print("I'm sorry, I couldn't find any more recipes matching your ingredients or categories. Please try again.")
                    current_recipe_index = 0 
                    repeated_recipe = False
        else:
            print("I'm sorry, I couldn't find any recipes matching your ingredients or categories. Please try again. Thank you.") 
            
chat()
