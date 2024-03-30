# Chatbot - Recipe Finder
Hello and welcome to the Chatbot "Recipe Finder". The Chatbot can help you to find the perfect recipe for you!
The search is based on your ingredients and preferences.

## Introduction
The Chatbot is implemented in Python. Users can enter their ingredients and preferences using the input function, and the Chatbot provides recipe recommendations tailored to their input. Natural language processing (NLP) techniques are used by the chatbot to accurately process user input.

### Clone the repository
Clone the repository to your local machine:
1. Open your terminal prompt
2. Navigate to the folder where you want to put the project files.
3. Use: 
```bash
git clone https://github.com/Maloulou99/Chatbot.git
```

4. Press Enter to run the command.
5. Wait for GitHub to clone the repository to your local machine. And now you should have a local copy of the project files ready to use.

## Installation
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

#### Download NLTK data
Also make sure you have downloaded the necessary NLTK data. You can download it using the following commands:

```bash
python -m nltk.downloader punkt
python -m nltk.downloader stopwords
python -m nltk.downloader wordnet
```

## Usage 
To use the "Recipe Finder" Chatbot correct, follow these steps: 
1. Run the chatbot.py script:
```bash
python chatbot.py
```
2. Follow the Chatbots prompt and add your ingredients and preferences.
3. Recipe Finder will process the information you have entered and provide you with a recipe recommendation based on the ingredients you have available. 
4. Type exit when you're finished. This will signal to the chatbot that you have received a recipe that suits you.

## Data
Recipe Finder uses a CSV file of recipes and their ingredients. 

If you'd like to replace the CSV file in the repository with your own CSV file of recipes. 
Navigate to line 82 of the chatbot.py script: 
```python
#DataCSV file
df = pd.read_csv('name_your_csv')
```
Replace 'name_your_csv' with the filename of your custom CSV file. Ensure that your CSV file follows the same format as the example provided.

## Contributing
If you'd like to contribute to Recipe Finder, feel free to the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

[MIT](https://choosealicense.com/licenses/mit/)
