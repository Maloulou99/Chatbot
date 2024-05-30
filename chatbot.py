import pandas as pd
import enchant
from text_processing import preprocess_input, stem, lemmatize, filter_for_stop_words, correct_spelling
from nltk.corpus import stopwords
import re

def contains_yes_or_no(input_text):
    input_text = input_text.lower()
    if re.search(r'\byes\b', input_text):
        return 'yes'
    elif re.search(r'\bno\b', input_text):
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
    total_correct = len(correct_recipes) 

    incorrect_count = total_recommended - correct_count

    accuracy = correct_count / total_correct if total_correct > 0 else 0
    return accuracy, incorrect_count

def adjust_recipe_for_persons(recipe, num_persons):
    adjusted_recipe = {}
    for key, value in recipe.items():
        if key == 'Ingredient':
            adjusted_ingredients = []
            ingredients = value.split('\n')
            for ingredient in ingredients:
                adjusted_ingredient = ingredient
                matches = re.findall(r'(\d+)', ingredient)
                for match in matches:
                    quantity = int(match)
                    adjusted_quantity = quantity * num_persons
                    adjusted_ingredient = adjusted_ingredient.replace(match, str(adjusted_quantity), 1)
                adjusted_ingredients.append(adjusted_ingredient)
            adjusted_recipe[key] = '\n'.join(adjusted_ingredients)
        else:
            adjusted_recipe[key] = value
    return adjusted_recipe

def get_matching_recipes(user_input, data): 
    user_tokens = preprocess_input(user_input)
    exclusions = extract_exclusions(user_input)
    matching_recipes = []
    for recipe in data:
        match_counter = 0
        recipe_description = ' '.join(str(v) for k, v in recipe.items() if k not in ['DishName', 'Step', 'Keywords', 'Category'])
        recipe_tokens = preprocess_input(recipe_description)
        if any(exclusion in recipe_tokens for exclusion in exclusions):
            continue
        for user_token in user_tokens:
            if user_token in recipe_tokens:
                match_counter += 1
        matching_recipes.append(recipe)
    if matching_recipes:
        return matching_recipes

def extract_num_persons(user_input):
    match = re.search(r'\b(\d+)\b', user_input)
    if match:
        return int(match.group(1))
    return 1  # Default to 1 person if no number is found

current_recipe_index = 0
repeated_recipe = False

def chat():
    global current_recipe_index, repeated_recipe
    print("Hello, I hope you are doing well! Welcome to your personal Recipe Finder!")
    print("You can tell me which ingredients or categories you have, and I can provide you with recipes based on those.")
    print("You can also specify ingredients to exclude by saying 'without [ingredient]' or 'no [ingredient]'.")
    print("Please write 'exit' when you are finished!")

    df = pd.read_csv('csv/recipe.csv')
    data = df.to_dict(orient='records')

    all_words = list(set(df['Keywords'].str.lower().str.split().sum()))
    processed_all_words = stem(all_words)
    processed_all_words = lemmatize(processed_all_words)

    conversation = [] 
    prev_output = None
    recommended_recipes = []
    correct_recipes = []

    while True:
        user_input = input("You: ").lower() 

        if user_input == 'exit':
            print("Thank you, enjoy your meal! Goodbye and I hope to see you soon!")
            accuracy, incorrect_count = evaluate_accuracy(correct_recipes, recommended_recipes)
            print(f"Accuracy: {accuracy}")
            print(f"Incorrect count: {incorrect_count}")
            print("Recommendations Recipe list:")
            for recipe in correct_recipes:
                print(recipe)
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

        processed_input = preprocess_input(user_input)
        processed_input = filter_for_stop_words(processed_input, stop_words)  
        processed_input = stem(processed_input)
        processed_input = lemmatize(processed_input)
        matching_recipes = get_matching_recipes(user_input, data)  

        if matching_recipes:
            if current_recipe_index < len(matching_recipes):
                print("Based on your ingredients or categories, here is a recipe recommendation:")
                print(matching_recipes[current_recipe_index]['DishName'])
                
                num_persons = extract_num_persons(user_input)
                adjusted_recipe = adjust_recipe_for_persons(matching_recipes[current_recipe_index], num_persons)
                print("Ingredients:")
                print(adjusted_recipe['Ingredient'])
                print("Steps:")
                print(adjusted_recipe['Step'])
                conversation.append(adjusted_recipe['Step'])

                recommended_recipes.append(matching_recipes[current_recipe_index]['DishName'])
                current_recipe_index += 1

            else:
                print("I have sent you all the recipes I have with your ingredients or categories.")
                repeat_response = input("Would you like to see a recipe again?\nYou: ").lower()
                repeat_response = contains_yes_or_no(repeat_response)
                if repeat_response == 'yes':
                    current_recipe_index = 0 
                    print("Here is the next recipe recommendation:")
                    print(matching_recipes[current_recipe_index]['DishName'])
                    num_persons = extract_num_persons(user_input)
                    adjusted_recipe = adjust_recipe_for_persons(matching_recipes[current_recipe_index], num_persons)
                    print("Ingredients:")
                    print(adjusted_recipe['Ingredient'])
                    print("Steps:")
                    print(adjusted_recipe['Step'])
                    conversation.append(adjusted_recipe['Step'])
                elif repeat_response == 'no':
                    input("DishDive: Anything else I can help you with?\nYou: ")
                else:
                    input("DishDive: I'm sorry, I didn't understand that.\nYou: ")

        else:
            print("I'm sorry, I couldn't find any recipes matching your ingredients or categories. Please try again. Thank you.") 

        add_recipe_response = input("Would you like to add any of these recipes to your correct recipes list?\nYou: ").strip().lower()
        add_recipe_response = contains_yes_or_no(add_recipe_response)

        if add_recipe_response == 'yes':
            if matching_recipes[current_recipe_index]['DishName'] not in correct_recipes:
                correct_recipes.append(matching_recipes[current_recipe_index]['DishName'])
                print("DishDive: Recipe added to your correct recipes list.")
            else:
                print("DishDive: This recipe is already in your correct recipes list.")
        elif add_recipe_response == 'no':
            print("DishDive: Okay, moving on.")
        else:
            print("DishDive: I'm sorry, I didn't understand that.")

chat()
