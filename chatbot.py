import pandas as pd
import enchant
import re
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

def preprocess_input_chat(input_text):
    tokens = nltk.word_tokenize(input_text)

    tokens_lower = [token.lower() for token in tokens]
    
    return tokens_lower

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
 

# Initialize the English dictionary for spell checking
spell_checker = enchant.Dict("en_US")

stop_words = set(stopwords.words('english'))

# Function to count matched columns from the user input
def count_matched_tokens(user_tokens, recipe_tokens):
    set1 = set(user_tokens)
    set2 = set(recipe_tokens)

    total_matches = len(set1.intersection(set2))

    return total_matches

# Function to extract exclusion ingredients from the user input
def extract_exclusions(user_input):
    exclusion_keywords = ["without", "no"]
    exclusions = []

    words = user_input.split()
    for i, word in enumerate(words):
        if word in exclusion_keywords and i + 1 < len(words):
            exclusions.append(words[i + 1])

    return exclusions

def evaluate_accuracy(correct_recipes, recommended_recipes):
    correct_count = sum(recipe in correct_recipes for recipe in recommended_recipes)
    total_recommended = len(recommended_recipes)
    incorrect_count = total_recommended - correct_count
    return correct_count, total_recommended, incorrect_count

def adjust_recipe_for_persons(recipe, num_persons):
    adjusted_recipe = {}
    
    for key, value in recipe.items():
        if key == 'Ingredient':
            adjusted_ingredients = []
            ingredients = value.split(' ')
            for ingredient in ingredients:
                match = re.match(r'(\d+)([a-zA-Z]*)', ingredient)
                if match:
                    quantity = int(match.group(1))
                    unit = match.group(2)
                    adjusted_quantity = quantity * num_persons
                    adjusted_ingredients.append(f"{adjusted_quantity}{unit}")
                else:
                    adjusted_ingredients.append(ingredient)
            adjusted_recipe[key] = ' '.join(adjusted_ingredients)
        else:
            adjusted_recipe[key] = value
            
    return adjusted_recipe

def get_matching_recipes(user_input, data_filename):
    user_tokens = preprocess_input(user_input)
    exclusions = extract_exclusions(user_input)
    matching_recipes = []
    match_scores = {}  # Dictionary to store match scores for each recipe

    with open(data_filename, 'r') as file:
        for line in file:
            recipe = {}
            recipe_data = line.strip().split(',')
            recipe['DishName'] = recipe_data[0]
            recipe['Ingredient'] = recipe_data[1]
            recipe['Step'] = recipe_data[2]
            recipe['Keywords'] = recipe_data[3]
            recipe['Category'] = recipe_data[4]

            match_counter = 0
            recipe_description = ' '.join(recipe_data[1:4])  # Joining ingredient, step, and keywords
            recipe_tokens = preprocess_input(recipe_description)

            # Skip recipes that contain excluded ingredients
            if any(exclusion in recipe_tokens for exclusion in exclusions):
                continue

            for user_token in user_tokens:
                if user_token in recipe_tokens:
                    match_counter += 1

            # Check if user input matches recipe name
            if user_input.lower() in recipe['DishName'].lower():
                return [recipe]  

            matching_recipes.append(recipe)
            match_scores[recipe['DishName']] = match_counter

    # Sort matching recipes based on match scores
    matching_recipes.sort(key=lambda x: match_scores.get(x['DishName'], 0), reverse=True)

    return matching_recipes or matching_recipes == False


def extract_num_persons(input_text):
    match = re.search(r'\b(\d+)\b', input_text)
    return int(match.group(1)) if match else 1

def chat():
    global repeated_recipe
    print("Hello, I hope you are doing well! Welcome to your personal Recipe Finder!")
    print("You can tell me which ingredients or categories you have, and I can provide you with recipes based on those.")
    print("You can also specify ingredients to exclude by saying 'without [ingredient]' or 'no [ingredient]'.")
    print("Please write 'exit' when you are finished!")

    conversation = []
    prev_output = None
    recommended_recipes = []  

    while True:
        user_input = input("You: ").lower()

        if user_input == 'exit':
            print("Thank you, enjoy your meal! Goodbye and I hope to see you soon!")
            break  

        if user_input.strip() == '':
            print("I'm sorry, I couldn't detect any input. Please try again.")
            continue

        if prev_output != user_input:
            print("DishDive:", end=" ")

        conversation.append(user_input)
        corrected_input = correct_spelling(user_input)

        if corrected_input != user_input:
            user_input = corrected_input

        try:
            matching_recipes = get_matching_recipes(user_input, 'csv/recipe.csv')
        except ValueError as e:
            if matching_recipes is not False:
                print(e)
            continue

        if not matching_recipes:
            print("I'm sorry, I couldn't find any recipes matching your ingredients or categories. Please try again. Thank you.")
            continue  # Start the chat loop again if no recipes were found

        # Sort matching recipes based on match count
        matching_recipes.sort(key=lambda x: count_matched_tokens(preprocess_input(user_input), preprocess_input(x['Ingredient'])))
        new_matching_recipes = [recipe for recipe in matching_recipes if recipe['DishName'] not in recommended_recipes]
        
        if new_matching_recipes and new_matching_recipes[0]['DishName'] != 'DishName':
            print("Based on your ingredients or categories, here is a recipe recommendation:")
            print(new_matching_recipes[0]['DishName'])

            num_persons = extract_num_persons(user_input)
            adjusted_recipe = adjust_recipe_for_persons(new_matching_recipes[0], num_persons)
            print("Ingredients:")
            print(adjusted_recipe['Ingredient'])
            print("Steps:")
            print(adjusted_recipe['Step'])
            conversation.append(adjusted_recipe['Step'])

            recommended_recipes.append(new_matching_recipes[0]['DishName'])
        else:
            if not recommended_recipes:
                user_response = input("I'm sorry, there are no recipes matching your criteria. Would you like to try again or exit? \nYou: ").lower()
                user_response = correct_spelling(user_response)

                if contains_yes_or_no(user_response) == 'yes':
                    continue  # Start the chat loop again
                else:
                    break  # Exit the chat loop
            else:
                print("I'm sorry, there are no more recipes matching your criteria and previous recommendations.")
                user_response = input("Do you want to see a previous recipe again or change your criteria? \nYou: ").lower()
                user_response = correct_spelling(user_response)

                if contains_yes_or_no(user_response) == 'yes':
                    # Print the last recommended recipe again
                    last_recommended_recipe = recommended_recipes[-1]
                    for recipe in matching_recipes:
                        if recipe['DishName'] == last_recommended_recipe:
                            print("Here is the previous recipe recommendation again:")
                            print(recipe['DishName'])
                            print("Ingredients:")
                            print(recipe['Ingredient'])
                            print("Steps:")
                            print(recipe['Step'])
                            break
                else:
                    # Reset conversation and recommended recipes
                    conversation.clear()
                    recommended_recipes.clear()
                    print("You can start a new search now.")

    print("Thank you for using the Recipe Finder! Goodbye and have a great day!")

chat()
