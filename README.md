Text Analysis Pipeline (NLP)

A Python-based Natural Language Processing (NLP) pipeline for automated text extraction, cleaning, and sentiment analysis from online articles and web pages.
This project combines web scraping, text preprocessing, and linguistic scoring into a structured workflow that outputs detailed analytics to Excel.

Features
- Extracts text content from URLs using BeautifulSoup
- Cleans and tokenizes text with NLTK
- Removes extended stopword lists (generic, date, geographic, etc.)
- Lemmatizes words for consistency
- Calculates multiple readability and sentiment metrics:
  - Word, sentence, and syllable counts
  - Complex word and pronoun frequency
  - Average word and sentence lengths
  - Fog Index (readability score)
  - Polarity and Subjectivity scores

Tech Stack
- Python 3.8+
- Pandas – data handling and Excel I/O
- NLTK – tokenization, stopwords, lemmatization
- BeautifulSoup & Requests – web scraping
- Regex (re) – text cleaning

Setup Instructions
- Clone this repository:
  - git clone https://github.com/AnthonyRodrigues13/text-analysis-pipeline-nlp.git
  - cd text-analysis-pipeline-nlp
- Install dependencies:
  - pip install pandas nltk requests beautifulsoup4 openpyxl
- Add the required input files:
  - Input.xlsx → Contains a column named URL
  - Output Data Structure.xlsx → Template for output
  - Stopword and sentiment word lists (StopWords_*.txt, positive-words.txt, negative-words.txt)
- Run the script:
  - python main.py
- View the results in:
  - Output Data Structure.xlsx

Output
- The output Excel file includes:
  - Cleaned text
  - Linguistic metrics (word/syllable counts, Fog Index, etc.)
  - Sentiment analysis (positive, negative, polarity, subjectivity)
