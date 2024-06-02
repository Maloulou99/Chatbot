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

def get_matching_recipes(user_input, exclusions, data_filename):
    user_tokens = preprocess_input(user_input)
    exclusions = extract_exclusions(user_input)
    matching_recipes = []
    match_scores = {}

    data = []

    with open(data_filename, 'r') as file:
        for line in file:
            recipe = {}
            recipe_data = line.strip().split(',')
            recipe['DishName'] = recipe_data[0] if recipe_data[0] else ''
            recipe['Ingredient'] = recipe_data[1] if recipe_data[1] else ''
            recipe['Step'] = recipe_data[2] if recipe_data[2] else ''
            recipe['Keywords'] = recipe_data[3] if recipe_data[3] else ''
            if len(recipe_data) >= 5:
                recipe['Category'] = recipe_data[4]
            else:
                recipe['Category'] = ''

            data.append(recipe)

            # Combine all recipe data into a single string
            all_recipe_data = ' '.join(recipe_data)

            # Skip recipes that contain excluded ingredients
            if any(exclusion in all_recipe_data for exclusion in exclusions):
                continue

            match_counter = 0

            # Check each column separately for matching tokens
            for column_data in recipe_data:
                # Preprocess column data to get tokens
                column_tokens = preprocess_input(column_data)
                
                # Check if any whole word from user input matches any whole word in column data
                if any(user_word == column_word for user_word in user_tokens for column_word in column_tokens):
                    match_counter += 1

            # Add recipe to matching recipes
            matching_recipes.append(recipe)
            match_scores[recipe['DishName']] = match_counter

            # Check if user input matches recipe name
            if user_input.lower() in recipe['DishName'].lower():
                return [recipe]

    # Sort matching recipes based on match scores
    matching_recipes.sort(key=lambda x: match_scores.get(x['DishName'], 0), reverse=True)
    print(match_scores)

    # Check if there are matching recipes
    if matching_recipes:
        return matching_recipes
    else:
        # If no matching recipes, return the recipe with the highest match score
        max_score_recipe = max(match_scores, key=match_scores.get)
        return [{'DishName': max_score_recipe, 'Ingredient': '', 'Step': '', 'Keywords': ''}]


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

def extract_exclusions(user_input):
    exclusion_patterns = re.compile(r"\b(?:without|no|excluded|exclude|omit)\b\s+([a-zA-Z\s]+?)(?:\s|$|,)")
    exclusions = exclusion_patterns.findall(user_input.lower())
    for exclusion in exclusions:
        user_input = user_input.replace(exclusion, "")
    lemmatized_exclusions = [lemmatize(exclusion) for exclusion in exclusions]
    return lemmatized_exclusions

def chat():
    global repeated_recipe
    print("Hello, I hope you are doing well! Welcome to your personal Recipe Finder!")
    print("You can tell me which ingredients or categories you have, and I can provide you with recipes based on those.")
    print("You can also specify ingredients to exclude by saying 'without [ingredient]' or 'no [ingredient]'.")
    print("Please write 'exit' when you are finished!")

    conversation = []
    exclusions = []
    prev_output = None
    recommended_recipes = []

    while True:
        user_input = input("You: ").lower()

        if user_input == 'exit':
            print("Thank you, enjoy your meal! Goodbye and I hope to see you soon!")
            break

        if user_input.strip() == '' or contains_yes_or_no(user_input) == 'yes' or contains_yes_or_no(user_input) == 'no':
            print("I'm sorry, I couldn't detect any valid input. Please try again.")
            continue

        if prev_output != user_input:
            print("DishDive:", end=" ")

        # Correct spelling
        corrected_input = correct_spelling(user_input)

        if corrected_input != user_input:
            user_input = corrected_input

        # Extract exclusions and update conversation and exclusion lists
        new_exclusions = extract_exclusions(user_input)
        if new_exclusions:
            exclusions.extend(new_exclusions)
            exclusions = list(set(exclusions))  # Remove duplicates
        else:
            # Check if the user input is already in the conversation
            if user_input not in conversation:
                conversation.append(user_input)

        # Try to find matching recipes if there's enough valid input
        if conversation:
            try:
                matching_recipes = get_matching_recipes(user_input, exclusions, 'csv/recipe.csv')
            except ValueError as e:
                if matching_recipes is not False:
                    print(e)
                continue

            if not matching_recipes:
                print("I'm sorry, I couldn't find any recipes matching your ingredients or categories. Please try again. Thank you.")
                continue  # Start the chat loop again if no recipes were found

            # Sort matching recipes based on match count
            matching_recipes.sort(key=lambda x: count_matched_tokens(preprocess_input(user_input), preprocess_input(x['Ingredient'])), reverse=True)
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

                recommended_recipes.append(new_matching_recipes[0]['DishName'])
            else:
                if not recommended_recipes:
                    print("I'm sorry, there are no recipes matching your criteria. Please try again.")
                    continue  # Start the chat loop again

                else:
                    print("I'm sorry, there are no more recipes matching your criteria and previous recommendations.")
                    user_response = input("Do you want to see a previous recipe again and change your criteria? \nYou: ").lower()
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
                        print("What else can I help you with? ")

        prev_output = user_input

    print("Thank you for using the Recipe Finder! Goodbye and have a great day!")
    print(conversation)
    print(recommended_recipes)

chat()
