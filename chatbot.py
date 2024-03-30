import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Meat and Fish
meat_fish_keywords = ['Chicken', 'Fish', 'Beef', 'Pork', 'Salmon', 'Cod', 
                      'Shrimp', 'Turkey', 'Lamb', 'Tuna', 'Bacon',
                      'Trout', 'Sardines', 'Duck', 'Ham', 'Sausage',
                      'Halibut', 'Crab', 'Octopus', 'Venison', 'Anchovies',
                      'Lobster', 'Haddock', 'Mussels', 'Swordfish', 'Quail',
                      'Buffalo', 'Catfish', 'Oysters', 'Snapper']

# Grains
grains_keywords = ['Rice', 'Pasta', 'Quinoa', 'Bulgur', 'Oats', 
                   'Bread', 'Noodles', 'Corn', 'Barley', 'Couscous',
                   'Wheat', 'Rye', 'Farro', 'Polenta', 'Sorghum',
                   'Millet', 'Amaranth', 'Buckwheat', 'Risotto', 'Orzo',
                   'Spelt', 'Teff', 'Kamut', 'Triticale', 'Emmer',
                   'Freekeh', 'Semolina', 'Basmati', 'Arborio']

# Dairy Products
dairy_keywords = ['Milk', 'Cheese', 'Butter', 'Cream', 'Yogurt', 
                  'Eggs', 'Cottage cheese', 'Sour cream', 'Parmesan', 'Feta',
                  'Mozzarella', 'Ricotta', 'Goat cheese', 'Brie', 'Cheddar',
                  'Gouda', 'Swiss cheese', 'Havarti', 'Camembert', 'Provolone',
                  'Blue cheese', 'Colby', 'Mascarpone', 'Limburger', 'Paneer',
                  'Quark', 'Velveeta', 'Muenster', 'Manchego']

# Fruits and Vegetables
fruits_vegetables_keywords = ['Apples', 'Bananas', 'Oranges', 'Strawberries', 'Blueberries', 'Spinach', 
                               'Tomatoes', 'Avocado', 'Lemons', 'Pineapples',
                               'Mangoes', 'Grapes', 'Watermelon', 'Cucumbers', 'Bell peppers',
                               'Peas', 'Carrots', 'Lettuce', 'Broccoli', 'Cauliflower',
                               'Zucchini', 'Potatoes', 'Onions', 'Garlic', 'Ginger',
                               'Kale', 'Brussels sprouts', 'Celery', 'Artichokes']

# Baking Supplies
baking_keywords = ['Flour', 'Sugar', 'Yeast', 'Baking powder', 'Chocolate', 'Vanilla extract', 
                   'Honey', 'Almond flakes', 'Nuts', 'Cinnamon sticks',
                   'Coconut flakes', 'Baking soda', 'Cocoa powder', 'Brown sugar', 'Powdered sugar',
                   'Cornstarch', 'Shortening', 'Cake flour', 'Molasses', 'Cream of tartar',
                   'Confectioners sugar', 'Granulated sugar', 'Light brown sugar', 'Dark brown sugar', 
                   'Milk powder','Pectin', 'Vanilla bean', 'Candied peel', 'Gelatin']

# Beverages
beverages_keywords = ['Water', 'Coffee', 'Tea', 'Juice', 'Soda', 'Wine', 'Beer', 
                      'Smoothies', 'Iced tea', 'Sports drinks',
                      'Lemonade', 'Milkshake', 'Hot chocolate', 'Margarita', 'Mojito',
                      'Sangria', 'Mimosa', 'Martini', 'Pina colada', 'Irish coffee',
                      'Mai tai', 'Mint julep', 'Bloody Mary', 'Piña colada', 'White Russian',
                      'Cosmopolitan', 'Long Island iced tea', 'Whiskey sour', 'Mudslide']

# Sweet Ingredients
sweet_keywords = ['Sugar', 'Honey', 'Maple syrup', 'Brown sugar', 'Vanilla', 
                  'Chocolate', 'Caramel', 'Marshmallows', 'Fruit preserves', 'Condensed milk',
                  'Butterscotch', 'Agave nectar', 'Candy canes', 'Toffee', 'Pralines',
                  'Molasses', 'Rock candy', 'Buttercream', 'Jellybeans', 'Cotton candy',
                  'Gum drops', 'Lollipop', 'Frosting', 'Candied ginger', 'Marzipan',
                  'Turkish delight', 'Fudge', 'Sugar cubes', 'Caramel sauce', 'Butter toffee']

# Sour Ingredients
sour_keywords = ['Lemon', 'Lime', 'Vinegar', 'Yogurt', 'Sour cream', 'Buttermilk', 
                 'Sour cherries', 'Tamarind', 'Sour apples', 'Sour candies',
                 'Rhubarb', 'Gooseberries', 'Kiwi', 'Sour orange', 'Grapefruit',
                 'Green apple', 'Sour grapes', 'Sour plum', 'Sour cherry', 'Sour grape',
                 'Sour blueberries', 'Sour apricot', 'Sour raspberry', 'Sour mango', 'Sour peach',
                 'Sour papaya', 'Sour pineapple', 'Sour strawberry', 'Sour banana', 'Sour pear']

# Spices
spices_keywords = ['Black pepper', 'Cayenne pepper', 'Chili powder', 'Cumin', 'Curry powder', 
                   'Paprika', 'Red pepper flakes', 'Wasabi', 'Ginger', 'Mustard powder', 
                   'Horseradish', 'Szechuan pepper', 'Jalapeno', 'Tabasco', 'Harissa', 
                   'Sriracha', 'Habanero', 'Chipotle', 'Ghost pepper', 'Scotch bonnet']


# Initializations and downloads
stop_words = set(stopwords.words('english'))

# Function to preprocess user input
def preprocess_input(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in string.punctuation]
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

# Function to count matched ingredients
def count_matched_ingredients(tokens, keywords):
    set1 = set(tokens)
    set2 = set(keywords)

    # Count the number of matches
    count = len(set1.intersection(set2))
    
    return count

def find_keywords(tokens, keywords):
    matched_keywords = [token for token in tokens if token in keywords]
    return matched_keywords

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


# Main chat function
def chat():
    print("Hello, I hope you are doing well! Welcome to your personal Recipe Finder!")
    print("You can tell me which ingredients you have, and I can provide you with recipes based on those ingredients.")
    print("So let's start, what ingredients do you have?")
    print("Please write 'exit' when you are finished!")

    # Load recipe data from CSV
    df = pd.read_csv('recipies.csv')
    data = df.to_dict(orient='records')

    while True:
        user_input = input("You: ").lower() 

        if user_input == 'exit':
            print("Thank you, enjoy your meal! Goodbye and I hope to see you soon!")
            break

        processed_input = preprocess_input(user_input)
        processed_input = filter_for_stop_words(processed_input, stop_words)
        processed_input = stem(processed_input)
        processed_input = lemmatize(processed_input)
        keywords_all = meat_fish_keywords + grains_keywords + dairy_keywords + fruits_vegetables_keywords + baking_keywords + beverages_keywords + sweet_keywords + sour_keywords + spices_keywords
        keywords_all = filter_for_stop_words(keywords_all, stop_words)
        keywords_all = stem(keywords_all)
        keywords_all = lemmatize(keywords_all)
       
        processed_input = find_keywords(processed_input, keywords_all)

        if not processed_input:
            print("I'm sorry, I didn't understand that ingredient. Please try again.")
            continue

        max_match = 0
        indexer = 0
        index_of_max = 0

        for i in data:
            ingredient_string = i['Ingredient']
            ingredient_token_list = preprocess_input(ingredient_string)
            ingredient_token_list = filter_for_stop_words(ingredient_token_list, stop_words)
            ingredient_token_list = stem(ingredient_token_list)
            ingredient_token_list = lemmatize(ingredient_token_list)

            match_counter = count_matched_ingredients(processed_input, ingredient_token_list)
            if(max_match < match_counter):
                max_match = match_counter
                index_of_max = indexer
            indexer += 1

        print("Based on your ingredients, here's a recipe recommendation:")
        print(data[index_of_max]['Step'])
chat()
