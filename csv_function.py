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
    categories_df['Category'] = categories_df['Category'].astype(str)
    keywords_df['Keywords'] = keywords_df['Keywords'].astype(str)

    category_keywords = {}

    for index, row in keywords_df.iterrows():
        keyword = row['Keywords']
        category = row['Category']
        if category not in category_keywords:
            category_keywords[category] = []
        category_keywords[category].append(keyword)

    for index, row in categories_df.iterrows():
        category = row['Category']
        keywords = row['Keywords'].split()
        if category in category_keywords:
            category_keywords[category].extend(keywords)
        else:
            category_keywords[category] = keywords

    for index, row in recipes_df.iterrows():
        dish_name = str(row['DishName'])
        dish_keywords = row['Keywords'].split() if isinstance(row['Keywords'], str) else []
        matching_categories = []
        for category, keywords_list in category_keywords.items():
            if isinstance(category, str) and isinstance(dish_name, str):
                if any(keyword.lower() in dish_name.lower() for keyword in keywords_list):
                    dish_keywords.extend(keywords_list)
                    matching_categories.append(category)
        dish_keywords = list(set(dish_keywords))
        recipes_df.at[index, 'Keywords'] = ' '.join(dish_keywords)
        recipes_df.at[index, 'Category'] = ', '.join(matching_categories)

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
