import pandas as pd

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
        keywords = row['Keywords'].split()
        category_keywords[category] = keywords
        print(f"(1) Category: {category}, Keywords: {keywords}")
        print(" ----------------------------------")

    recipes_df['Category'] = '' #Delete the kolone for test
    recipes_df['Keywords'] = ''

    for index, row in recipes_df.iterrows():
        dish_name = row['DishName']
        matching_categories = []
        dish_keywords = []
        for category, keywords_list in category_keywords.items():
            if any(keyword.lower() in dish_name.lower() for keyword in keywords_list):
                matching_categories.append(category)
                dish_keywords.extend(keywords_list)
        dish_keywords = list(set(dish_keywords))
        recipes_df.at[index, 'Keywords'] = ' '.join(dish_keywords)
        recipes_df.at[index, 'Category'] = ', '.join(matching_categories)
        print(f"(2) Dish: {dish_name}, Categories: {matching_categories}, Keywords: {dish_keywords}\n")
        print(" ----------------------------------")

    for index, row in keywords_df.iterrows():
        dish_name = row['DishName']
        dish_keywords = row['Keywords']
        dish_category = row['Category']
        if isinstance(dish_keywords, str):
            matching_row = recipes_df[recipes_df['DishName'] == dish_name]
            if not matching_row.empty:
                current_keywords = matching_row['Keywords'].iloc[0]
                if isinstance(current_keywords, str):
                    current_keywords += ' ' + dish_keywords
                else:
                    current_keywords = dish_keywords
                recipes_df.at[matching_row.index[0], 'Keywords'] = current_keywords
                print(f"(3) Dish: {dish_name}, Keywords: {dish_keywords}, Category: {dish_category}\n")
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
