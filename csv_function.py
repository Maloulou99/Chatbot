import pandas as pd
from text_processing import preprocess_input, stem, lemmatize

def add_keywords_by_category():
    recipes_file = 'csv/recipe.csv'
    keywords_file = 'csv/keyword.csv'
    categories_file = 'csv/category.csv'

    recipes_df = pd.read_csv(recipes_file)
    keywords_df = pd.read_csv(keywords_file)
    categories_df = pd.read_csv(categories_file)

    if recipes_df.empty or keywords_df.empty or categories_df.empty:
        return None

    recipes_df['Keywords'] = recipes_df['Keywords'].astype(str)

    category_keywords = {}

    for index, row in categories_df.iterrows():
        category = row['Category']
        keywords = preprocess_input(row['Keywords'])
        stemmed_keywords = stem(keywords)
        lemmatized_keywords = lemmatize(keywords)
        combined_keywords = set(keywords + stemmed_keywords + lemmatized_keywords)
        category_keywords[category] = combined_keywords
        print(f"Category: {category}, Combined Keywords: {combined_keywords}")
        print(" ----------------------------------")


    recipes_df['Category'] = '' 
    recipes_df['Keywords'] = ''  

    for index, row in recipes_df.iterrows():
        dish_name = row['DishName']
        dish_tokens = preprocess_input(dish_name)
        stemmed_dish_tokens = stem(dish_tokens)
        lemmatized_dish_tokens = lemmatize(dish_tokens)
        combined_dish_tokens = set(dish_tokens + stemmed_dish_tokens + lemmatized_dish_tokens)

        matching_categories = set()
        dish_keywords = set()

        for category, keywords_list in category_keywords.items():
            if any(keyword in combined_dish_tokens for keyword in keywords_list):
                matching_categories.add(category)
                dish_keywords.update(keywords_list)

        recipes_df.at[index, 'Keywords'] = ' '.join(dish_keywords)
        recipes_df.at[index, 'Category'] = ', '.join(matching_categories)

        print(f"(2) Dish: {dish_name}, Categories: {matching_categories}, Keywords: {dish_keywords}\n")
        print(" ----------------------------------")


    for index, row in keywords_df.iterrows():
        dish_name = row['DishName']
        additional_keywords = preprocess_input(row['Keywords'])
        stemmed_additional_keywords = stem(additional_keywords)
        lemmatized_additional_keywords = lemmatize(additional_keywords)
        combined_additional_keywords = set(additional_keywords + stemmed_additional_keywords + lemmatized_additional_keywords)

        matching_row = recipes_df[recipes_df['DishName'] == dish_name]

        if not matching_row.empty:
            current_keywords = set(matching_row['Keywords'].iloc[0].split())
            current_categories = set(matching_row['Category'].iloc[0].split(', '))

            current_keywords.update(combined_additional_keywords)

            for keyword in combined_additional_keywords:
                for category, keywords_list in category_keywords.items():
                    if keyword in keywords_list:
                        current_categories.add(category)

            updated_keywords = ' '.join(current_keywords)
            updated_categories = ', '.join(filter(None, current_categories))
            recipes_df.at[matching_row.index[0], 'Keywords'] = updated_keywords
            recipes_df.at[matching_row.index[0], 'Category'] = updated_categories

            print(f"(3) Dish: {dish_name}, Additional Keywords: {additional_keywords}, Categories: {current_categories}\n")
            print(" ----------------------------------")

    recipes_df.to_csv(recipes_file, index=False)

    return recipes_df

def main():
    updated_recipes_df = add_keywords_by_category()

    if updated_recipes_df is not None:
        print(updated_recipes_df[['DishName', 'Keywords', 'Category']])
    else:
        print("Error: Unable to update recipes.")

if __name__ == "__main__":
    main()
