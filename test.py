import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
#import seaborn as sns

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

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


def find_keyword_list(user_input):
    user_input = user_input.lower()
    matching_lists = []

    if "meat" in user_input:
        matching_lists.extend(meat_fish_keywords)
    if "grains" in user_input:
        matching_lists.extend(grains_keywords)
    if "dairy" in user_input:
        matching_lists.extend(dairy_keywords)
    if any(word in user_input for word in ["fruits", "vegetables"]):
        matching_lists.extend(fruits_vegetables_keywords)
    if "baking" in user_input:
        matching_lists.extend(baking_keywords)
    if "beverages" in user_input:
        matching_lists.extend(beverages_keywords)
    if "sweet" in user_input:
        matching_lists.extend(sweet_keywords)
    if "sour" in user_input:
        matching_lists.extend(sour_keywords)
    if "spices" in user_input:
        matching_lists.extend(spices_keywords)

    return matching_lists if matching_lists else None

#Seperate the words in a setting
""" def toktok_tokenize(data):
    toktok = nltk.ToktokTokenizer()
    toktok.tokenize
    toktok = [token for token in toktok if token not in string.punctuation]
    #data = data.translate(str.maketrans('', '', string.punctuation))
    #toktok = toktok.tokenize(data)
    return toktok """

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

#Categorize the words to grammatical tagging
def post_tagging(words):
    tags = nltk.pos_tag(words)
    nouns = [token for token, pos in tags if pos.startswith('N')]
    verbs = [token for token, pos in tags if pos.startswith('V')]
    adverbs = [token for token, pos in tags if pos.startswith('W')]
    return nouns, verbs, adverbs

#Processing the user inputs with the chatbot
def preprocess_input(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token for token in tokens if token not in string.punctuation]

    tokens = [token for token in tokens if token.lower() not in stop_words]
    return tokens

def find_keywords(tokens, keywords):
    matched_keywords = [token for token in tokens if token.capitalize() in keywords]
    return matched_keywords

# Seperate the words
def toktok_tokenize_recipe(data):
    toktok = nltk.ToktokTokenizer()
    toktok_tokens = [toktok.tokenize(recipe['Step list']) for recipe in data]
    return toktok_tokens

# Count matched words
def count_matched_words(tokens, keywords):
    set1 = set(tokens)
    set2 = set(keywords)

    # Count the number of matches
    count = len(set1.intersection(set2))
    
    return count

def find_keywords(tokens, keywords):
    matched_keywords = [token for token in tokens if token.capitalize() in keywords]
    return matched_keywords
    

# Define a function to handle the conversation
def chat():
    print("Helloooo, I hope you are doing well! Welcome to your personal Recipe Finder!")
    print("You can tell me which ingredients you have, and I can provide you with recipes based on those ingredients.")
    print("So let's start, what ingredients do you have?")
    print("Please write 'exit' when you are finished!")
    df = pd.read_csv('recipies.csv')
    data = df.to_dict(orient='records')
    while True:
        user_input = input("You: ").lower() 
        
       
        processed_input = preprocess_input(user_input)
        #toktok_tokenize(processed_input)
        
        # user_input = input("Enter keywords: ")
        # keyword_list = find_keyword_list(user_input)

        # if keyword_list:
        #     print("Matching keywords:")
        #     for keyword in keyword_list:
        #         print(keyword)
        # else:
        #     print("No matching keyword list found for the input.")

        filter_for_stop_words(processed_input, stop_words)
        stem(processed_input)
        lemmatize(processed_input)
        post_tagging(processed_input)
        print(processed_input)
        matched_keywords = find_keywords(processed_input, 
        meat_fish_keywords + grains_keywords + dairy_keywords + 
        fruits_vegetables_keywords + baking_keywords + beverages_keywords + 
        sweet_keywords + sour_keywords + spices_keywords)



        if user_input == 'exit':
            print("Thank you, enjoy your meal! Goodbye and I hope to see you soon!")
            break
    
    # Get keywords based on user input
      
        if matched_keywords is None:
            print("I'm sorry, I didn't understand that ingredient. Please try again.")
            continue

        print(f"The keywords for the '{user_input}' category are: {', '.join(matched_keywords)}")

       

        #DataCSV file
        

        max_match = 0
        indexer = 0
        index_of_max = 0

        for i in data:
            ingredient_string = i['Ingredient list']
            ingredient_token_list = preprocess_input(ingredient_string)
            filter_for_stop_words(ingredient_token_list, stop_words)
            stem(ingredient_token_list)
            lemmatize(ingredient_token_list)
            post_tagging(ingredient_token_list)

            match_counter = count_matched_words(matched_keywords, ingredient_token_list)
            if(max_match < match_counter):
                max_match = match_counter
                index_of_max = indexer
            indexer += 1

        print(index_of_max)


      
        #print(data)
        #Print the data out from the index
        #data[0] 
        
        #How many Index positions do we have in the CSV 
        #len(data)

        if processed_input:
            print("You mentioned:", ", ".join(processed_input))


            print("Based on your ingredients, here's a recipe recommendation:")
            print(data[index_of_max]['Step list'])
chat()

