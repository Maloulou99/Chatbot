# Chatbot - DishDive
The Chatbot "DishDive" can help you to find the perfect recipe for you!
The search is based on your ingredients and preferences. 

## Implementation
The Chatbot is implemented in Python. Users can enter their ingredients and preferences using the input function, and the Chatbot provides recipe recommendations tailored to their input. 
Natural language processing (NLP) techniques are used by the chatbot to accurately process user input.

## Installation
Clone the repository to your local machine:
Use: 
```bash
git clone https://github.com/Maloulou99/Chatbot.git
```

The following cell contains the Python libraries needed to work with the Chatbot. They need to be installed in the running environment with e.g:

```bash
pip install pandas
```

```python
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
```

### Download NLTK data
Also make sure you have downloaded the necessary NLTK data. You can download it using the following commands:

```bash
python -m nltk.downloader punkt
python -m nltk.downloader stopwords
python -m nltk.downloader wordnet
```

## Usage 
To use the "DishDive" Chatbot correct, follow these steps:
1. First run the csv_function.py script to update the recipe.csv file
2. Run the chatbot.py script:
```bash
python chatbot.py
```
3. Follow the Chatbots prompt and add your ingredients and preferences. DishDive will provide you with a recipe recommendation based on the your ingredients. 
4. Type exit when you're finished. This will signal to the Chatbot that you have received a recipe that suits you.

## Data
DishDive has three different CSV files:

recipe.csv - keyword.csv - category.csv

These files contain information about recipes, their ingredients, steps, keywords, and categories.

You have the flexibility to modify the data:

**recipe.csv**: Add new recipes along with their ingredients.
**keyword.csv**: Add general keywords for the recipe.
**category.csv**: View available categories and assign your recipes to appropriate categories. Additionally, link keywords to specific categories by adding the category name in the keyword.csv file.

Feel free to customize and enrich the data according to your preferences!

## License
You can use VSC program to clone the program for free - see the LICENSE file for details.

[MIT](https://choosealicense.com/licenses/mit/)
