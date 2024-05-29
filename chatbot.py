import pandas as pd
import enchant
from text_processing import preprocess_input, stem, lemmatize, filter_for_stop_words, correct_spelling
from nltk.corpus import stopwords

# Initialize the English dictionary for spell checking
spell_checker = enchant.Dict("en_US")

# Initialize stop words
stop_words = set(stopwords.words('english'))

# Function to count matched columns from the user input
def count_matched_tokens(user_tokens, recipe_tokens):
    set1 = set(user_tokens)
    set2 = set(recipe_tokens)

    total_matches = len(set1.intersection(set2))

    return total_matches

# Give the Chatbot a chance to send a new recipe to the same user input
def get_matching_recipes(user_input, data): 
    user_tokens = preprocess_input(user_input)
    matching_recipes = []

    for recipe in data:
        match_counter = 0
        recipe_description = ' '.join(str(v) for k, v in recipe.items() if k not in ['DishName', 'Step', 'Keywords', 'Category'])
        recipe_tokens = preprocess_input(recipe_description)

        for user_token in user_tokens:
            if user_token in recipe_tokens:
                match_counter += 1

        matching_recipes.append((recipe, match_counter))

    if matching_recipes:
        max_match_count = max(matching_recipes, key=lambda x: x[1])[1]
        top_matching_recipes = [recipe[0] for recipe in matching_recipes if recipe[1] == max_match_count]

        return top_matching_recipes

current_recipe_index = 0
repeated_recipe = False


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

    conversation = [] 
    prev_output = None

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

        # Perform spell checking and correct spelling
        corrected_input = correct_spelling(user_input)

        # If the corrected input is different from the original input
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
                print(matching_recipes[current_recipe_index]['Step'])
                conversation.append(matching_recipes[current_recipe_index]['Step'])

                current_recipe_index =+ 1

            else:
                print("I have sent you all the recipes I have with your ingredients or categories.")
                repeat_response = input("Would you like to see a recipe again?\nYou: ").lower()
                if repeat_response == 'yes':
                    current_recipe_index = 0 
                    print("Here is the next recipe recommendation:")
                    print(matching_recipes[current_recipe_index]['DishName'])
                    print(matching_recipes[current_recipe_index]['Step'])
                    conversation.append(matching_recipes[current_recipe_index]['Step'])
                    
        else:
            print("I'm sorry, I couldn't find any recipes matching your ingredients or categories. Please try again. Thank you.") 

chat()
