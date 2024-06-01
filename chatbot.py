import re
from text_processing import preprocess_input, contains_yes_or_no, count_matched_tokens, extract_num_persons, extract_exclusions, correct_spelling

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
    match_scores = {}  

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

            # Check each column separately for matching tokens
            for column_data in recipe_data:
                column_tokens = preprocess_input(column_data)
                if any(user_token in column_tokens for user_token in user_tokens):
                    match_counter += 1

            # Skip recipes that contain excluded ingredients
            if any(exclusion in preprocess_input(recipe_data[1]) for exclusion in exclusions):
                continue

            # Check if user input matches recipe name
            if user_input.lower() in recipe['DishName'].lower():
                return [recipe]  

            matching_recipes.append(recipe)
            match_scores[recipe['DishName']] = match_counter

    # Sort matching recipes based on match scores
    matching_recipes.sort(key=lambda x: match_scores.get(x['DishName'], 0), reverse=True)

    return matching_recipes or matching_recipes == False

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
                print("I'm sorry, there are no recipes matching your criteria. Please try again.")
                continue  # Start the chat loop again
                
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
                    print("What else can i help you with? ")

    print("Thank you for using the Recipe Finder! Goodbye and have a great day!")

chat()
