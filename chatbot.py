import re
from text_processing import preprocess_input, contains_yes_or_no, count_matched_tokens, extract_num_persons, lemmatize, stem
from enchant.checker import SpellChecker

def extract_ingredients(line):
    ingredients = re.findall(r'\b(\d+)\s*(\w+)\b', line)
    lemmatized_ingredients = [(quantity, lemmatize(ingredient)) for quantity, ingredient in ingredients]
    return lemmatized_ingredients

def filter_recipes_by_ingredient(recipes, ingredient):
    filtered_recipes = []
    stemmed_ingredient = stem(ingredient.lower())
    for recipe in recipes:
        if stemmed_ingredient in stem(recipe['Ingredient'].lower()):
            filtered_recipes.append(recipe)
    return filtered_recipes

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
    
def get_matching_recipes(user_input, positive_list, negative_list, data_filename):
    user_tokens = preprocess_input(user_input)
    matching_recipes = []
    match_scores = {}

    with open(data_filename, 'r') as file:
        for line in file:
            recipe = {}
            recipe_data = line.strip().split(',')
            recipe['DishName'] = recipe_data[0] if recipe_data[0] else ''
            recipe['Ingredient'] = recipe_data[1] if recipe_data[1] else ''
            recipe['Step'] = recipe_data[2] if recipe_data[2] else ''
            recipe['Keywords'] = recipe_data[3] if recipe_data[3] else ''
            recipe['Category'] = recipe_data[4] if len(recipe_data) >= 5 else ''

            # Combine all recipe data into a single string
            all_recipe_data = ' '.join(recipe_data)

            # Skip recipes that contain excluded ingredients from the negative list
            if any(negative_match in all_recipe_data for negative_match in negative_list):
                continue

            match_counter = 0

            # Check each column separately for matching tokens
            for column_data in recipe_data:
                # Preprocess column data to get tokens
                column_tokens = preprocess_input(column_data)

                # Check if any whole word from user input matches any whole word in column data
                for user_word in user_tokens:
                    for column_word in column_tokens:
                        if user_word == column_word:
                            match_counter += 1

            # Check if there are positive matches and no negative matches
            if match_counter > 0 and all(positive_match in all_recipe_data for positive_match in positive_list) and not any(negative_match in all_recipe_data for negative_match in negative_list):
                matching_recipes.append(recipe)
                match_scores[recipe['DishName']] = match_counter

    # Sort matching recipes based on match scores
    matching_recipes.sort(key=lambda x: match_scores.get(x['DishName'], 0), reverse=True)

    return matching_recipes

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

import re

def chat():
    print("Hello, I hope you are doing well! Welcome to your personal Recipe Finder!")
    print("You can tell me which ingredients or categories you have, and I can provide you with recipes based on those.")
    print("Please write 'exit' when you are finished!")

    conversation = []
    positive_list = []
    negative_list = []
    prev_output = None
    recommended_recipes = []
    matching_recipes = []

    while True:
        user_input = input("You: ").lower()

        if user_input == 'exit':
            print("Thank you, enjoy your meal! Goodbye and I hope to see you soon!")
            break

        if user_input.strip() == '':
            print("I'm sorry, I couldn't detect any valid input. Please try again.")
            continue

        if prev_output != user_input:
            print("DishDive:", end=" ")

        # Extract positive and negative ingredients from user input
        positive_ingredients = re.findall(r'\b(?:with|contains|want|love|wish?)\s(\w+)\b', user_input)
        negative_ingredients = re.findall(r"\b(?:no|without|don't\slike|dislike)\s(\w+)\b", user_input)

        # Handle simple ingredient inputs
        if not positive_ingredients and not negative_ingredients:
            if 'with' in user_input:
                ingredient = user_input.split('with')[-1].strip()
                if ingredient in negative_list:
                    negative_list.remove(ingredient)
                positive_list.append(ingredient)
            elif 'no' in user_input:
                ingredient = user_input.split('no')[-1].strip()
                if ingredient in positive_list:
                    positive_list.remove(ingredient)
                negative_list.append(ingredient)
            else:
                # Handle simple single ingredient input
                if ' and ' in user_input:
                    positive_ingredients = user_input.split(' and ')
                else:
                    positive_ingredients = [user_input]
        else:
            # Remove ingredients specified as negative from the positive list
            for ingredient in positive_ingredients:
                if ingredient in negative_list:
                    negative_list.remove(ingredient)
            # Remove ingredients specified as positive from the negative list
            for ingredient in negative_ingredients:
                if ingredient in positive_list:
                    positive_list.remove(ingredient)

        # Update positive and negative lists
        positive_list.extend(positive_ingredients)
        negative_list.extend(negative_ingredients)

        # Remove duplicates from lists
        positive_list = list(set(positive_list))
        negative_list = list(set(negative_list))

        # Try to find matching recipes if there's enough valid input
        if positive_list or negative_list:
            try:
                matching_recipes = get_matching_recipes(user_input, positive_list, negative_list, 'csv/recipe.csv')
            except ValueError as e:
                if matching_recipes:
                    print(e)
                continue

            if not matching_recipes:
                print("I'm sorry, I couldn't find any recipes matching your ingredients or categories.")
                continue

            # Filter out already recommended recipes
            new_matching_recipes = [recipe for recipe in matching_recipes if recipe['DishName'] not in recommended_recipes]

            if new_matching_recipes and new_matching_recipes[0]['DishName'] != 'DishName':
                next_recipe = new_matching_recipes[0]
                recommended_recipes.append(next_recipe['DishName'])

                num_persons = extract_num_persons(user_input)
                next_recipe = adjust_recipe_for_persons(next_recipe, num_persons)
                print("\nBased on your ingredients or categories, here is a recipe recommendation:")
                print(f"Dish Name: {next_recipe['DishName']}")
                print("Ingredients:")
                print(next_recipe['Ingredient'])
                print("Steps:")
                print(next_recipe['Step'])
            else:
                print("I'm sorry, there are no more recipes matching your criteria and previous recommendations.")
                user_response = input("Do you want to see a previous recipe again and change your criteria? \nYou: ").lower()
                user_response = correct_spelling(user_response)

                if contains_yes_or_no(user_response) == 'yes':
                    # Print the last recommended recipe again
                    last_recommended_recipe = recommended_recipes[-1]
                    for recipe in matching_recipes:
                        if recipe['DishName'] == last_recommended_recipe:
                            adjusted_recipe = adjust_recipe_for_persons(recipe, num_persons)
                            print("\nHere is the previous recipe recommendation again:")
                            print(f"Dish Name: {adjusted_recipe['DishName']}")
                            print("Ingredients:")
                            print(adjusted_recipe['Ingredient'])
                            print("Steps:")
                            print(adjusted_recipe['Step'])
                            break
                else:
                    # Reset conversation and recommended recipes
                    conversation.clear()
                    positive_list.clear()
                    negative_list.clear()
                    recommended_recipes.clear()
                    matching_recipes.clear()
                    print("What else can I help you with? ")

        prev_output = user_input

    print("\nThank you for using the Recipe Finder! Goodbye and have a great day!")
    print("Conversation log:", conversation)
    print("Positiv log:", positive_list)
    print("Negativ log:", negative_list)
    print("Recommended recipes log:", recommended_recipes)

chat()
