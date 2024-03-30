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

# Function to count matched ingredients
def count_matched_ingredients(recipe, ingredients):
    count = 0
    for ingredient in recipe['Ingredient'].split(','):
        if any(keyword in ingredient for keyword in ingredients):
            count += 1
    return count

# Main chat function
def chat():
    print("Hello, I hope you are doing well! Welcome to your personal Recipe Finder!")
    print("You can tell me which ingredients you have, and I can provide you with recipes based on those ingredients.")
    print("So let's start, what ingredients do you have?")
    print("Please write 'exit' when you are finished!")

    # Load recipe data from CSV
    df = pd.read_csv('recipes.csv')

    while True:
        user_input = input("You: ").lower() 

        if user_input == 'exit':
            print("Thank you, enjoy your meal! Goodbye and I hope to see you soon!")
            break

        processed_input = preprocess_input(user_input)

        if not processed_input:
            print("I'm sorry, I didn't understand that ingredient. Please try again.")
            continue

        print(f"The ingredients you mentioned are: {', '.join(processed_input)}")

        # Count matched ingredients for each recipe
        df['Matched Ingredients'] = df.apply(lambda x: count_matched_ingredients(x, processed_input), axis=1)

        # Find recipe with maximum matched ingredients
        max_matched_recipe_index = df['Matched Ingredients'].idxmax()

        print("Based on your ingredients, here's a recipe recommendation:")
        print(df.loc[max_matched_recipe_index, 'Step'])

# Run the chat function
chat()
