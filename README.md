# Chatbot - Recipe Finder
Hello and welcome to the Chatbot "Recipe Finder". The Chatbot can help you to find the perfect recipe for you!
The search is based on your ingredients and preferences.

## Introduction
The chatbot is implemented in Python. Users can enter their ingredients and preferences using the input function, and the chatbot provides recipe recommendations tailored to their input. Natural language processing (NLP) techniques are used by the chatbot to accurately process user input.

### Clone the repository
Clone the repository to your local machine:
1. Open your terminal prompt
2. Navigate to the folder where you want to put the project files.
3. Use: 
```bash
git clone <repository_url> 
```
Replace <repository_url> with the URL of the repository you want to clone. You can find this URL on the repository's GitHub page under the "Clone or download" button. 

4. Press Enter to run the command.
5. Wait for GitHub to clone the repository to your local machine. And now you should have a local copy of the project files ready to use.

### Install the required Python libraries
The following cell contains the Python libraries needed to work with the chatbot. They need to be installed in the running environment with e.g:

```bash
pip install pandas
```

```bash
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
```

#### Download NLTK data
Also make sure you have downloaded the necessary NLTK data. You can download it using the following commands:

```bash
python -m nltk.downloader punkt
python -m nltk.downloader stopwords
python -m nltk.downloader wordnet
```

Run the recipe_finder.py script:

python recipe_finder.py
Follow the prompts to input the ingredients you have. Type exit when you're finished.

Recipe Finder will process your input and provide you with a recipe recommendation based on the ingredients you have.

## Data
Recipe Finder uses a CSV file containing recipes and their ingredients. You can replace the name_your_csv file in the repository with your own CSV file containing recipes.

## Contributing
If you'd like to contribute to Recipe Finder, feel free to fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
