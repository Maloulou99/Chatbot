import pandas as pd
from text_processing import preprocess_input, stem, lemmatize, filter_for_stop_words, count_matched_tokens

# Function to get matching recipes based on user input
def get_matching_recipes(user_tokens, data): 
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

    return []

current_recipe_index = 0
previous_user_tokens = []

# Main Chatbot chat
def chat():
    global current_recipe_index, previous_user_tokens
    print("Hello, I hope you are doing well! Welcome to your personal Recipe Finder!")
    print("You can tell me which ingredients or categories you have, and I can provide you with recipes based on those.")
    print("So let's start, what ingredients or categories do you have?")
    print("Please write 'exit' when you are finished!")

    df = pd.read_csv('csv/recipe.csv')
    data = df.to_dict(orient='records')

    conversation = [] 
    prev_output = None
    printed_keywords = False

    while True:
        user_input = input("You: ").lower() 

        if user_input == 'exit':
            print("Thank you, enjoy your meal! Goodbye and I hope to see you soon!")
            break

        if not user_input:
            print("DishDive: It seems you haven't entered anything. How can I assist you today?")
            continue

        if prev_output != user_input:
            print("DishDive:", end=" ")

        conversation.append(user_input) 

        # Process user input
        processed_input = preprocess_input(user_input)
        processed_input = filter_for_stop_words(processed_input)
        processed_input = stem(processed_input)
        processed_input = lemmatize(processed_input)

        previous_user_tokens.extend(processed_input)

        # Get matching recipes
        matching_recipes = get_matching_recipes(previous_user_tokens, data)  

        if matching_recipes:
            if current_recipe_index < len(matching_recipes):
                print("Based on your ingredients or categories, here is a recipe recommendation:")
                print(matching_recipes[current_recipe_index]['DishName'])
                print(matching_recipes[current_recipe_index]['Step'])
                conversation.append(matching_recipes[current_recipe_index]['Step'])
                current_recipe_index += 1 
            else:
                print("I have sent you all the recipes I have with your ingredients or categories.")
                if not printed_keywords:
                    unique_tokens = set(previous_user_tokens)
                    unique_tokens_list = list(unique_tokens)
                    print(f"You had searched on: {', '.join(unique_tokens_list)}")
                new_input = input("Would you like to search for something else?\nYou: ").lower()
                previous_user_tokens = preprocess_input(new_input)
                previous_user_tokens = filter_for_stop_words(previous_user_tokens)
                previous_user_tokens = stem(previous_user_tokens)
                previous_user_tokens = lemmatize(previous_user_tokens)
                printed_keywords = False

                if matching_recipes and new_input != 'exit':
                    print("DishDive: What else can I help you with? ", end="\n")
                    continue

chat()
