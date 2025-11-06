import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import cmudict
import re
import requests
from bs4 import BeautifulSoup


df_ip = pd.read_excel('Input.xlsx', usecols=['URL'])
df_op = pd.read_excel('Output Data Structure.xlsx')

lemma = WordNetLemmatizer()

def stopWord():
    s1 = stopwords.words('english')
    file = open('StopWords_Auditor.txt', 'r')
    s2 = file.read().split()
    file = open('StopWords_Currencies.txt', 'r')
    s3 = file.read().split()
    file = open('StopWords_DatesandNumbers.txt', 'r')
    s4 = file.read().split()
    file = open('StopWords_Generic.txt', 'r')
    s5 = file.read().split()
    file = open('StopWords_GenericLong.txt', 'r')
    s6 = file.read().split()
    file = open('StopWords_Geographic.txt', 'r')
    s7 = file.read().split()
    file = open('StopWords_Names.txt', 'r')
    s8 = file.read().split()
    stop_words = s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8
    return stop_words

def syllable_count(word):
    word =word.lower()
    count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count +=1
            if word.endswith("e") or word.endswith("es") or word.endswith("ed"):
                count -= 1
    if count == 0:
        count += 1
    return count

def syllableCount(x:str) -> list:
    corp = str(x).lower() 
    corp = re.sub('[^a-zA-Z]+',' ', corp).strip() 
    tokens = word_tokenize(corp)
    words = [t for t in tokens if t not in stop_words]
    lemmatize = [lemma.lemmatize(w) for w in words]
    syl_cnt = 0
    for w in lemmatize:
        syl = syllable_count(w)
        if syl > 1:
            syl_cnt = syl_cnt + syl  # total no of syllables
    return syl_cnt

def complexWord(x:str) -> list:
    corp = str(x).lower() 
    corp = re.sub('[^a-zA-Z]+',' ', corp).strip() 
    tokens = word_tokenize(corp)
    words = [t for t in tokens if t not in stop_words]
    lemmatize = [lemma.lemmatize(w) for w in words]
    com_word_cnt = 0    
    for w in lemmatize:
        syl = syllable_count(w)
        if syl > 1:
            com_word_cnt += 1  #no. of complex words
    return com_word_cnt

def text_prep(x: str) -> list:
     corp = str(x).lower() 
     corp = re.sub('[^a-zA-Z]+',' ', corp).strip() 
     tokens = word_tokenize(corp)
     words = [t for t in tokens if t not in stop_words]
     lemmatize = [lemma.lemmatize(w) for w in words]
     return lemmatize

def charCount(x:str) -> list:
    corp = str(x).lower()
    corp = re.sub('[^a-zA-Z]+',' ', corp).strip() 
    tokens = word_tokenize(corp)
    words = [t for t in tokens if t not in stop_words]
    lemmatize = [lemma.lemmatize(w) for w in words]
    c = 0
    for l in lemmatize:
        c = c + len(l)
    return c

def sentenceCount(x:str) -> list:
    corp = str(x).lower() 
    corp = re.sub('[^a-zA-Z]+',' ', corp).strip() 
    tokened_sentence = sent_tokenize(corp)
    return len(tokened_sentence)

def pronounCount(x:str) -> list:
    pronounRegex = re.compile(r'I|we|my|ours|us',re.I)
    corp = str(x).lower()
    corp = re.sub('[^a-zA-Z]+',' ', corp).strip()     
    pronouns = pronounRegex.findall(corp)
    for i in pronouns:
        if i == 'US':
            pronouns.remove(i)
    return len(pronouns)

def readURL(x:str) -> list:
    url=str(x)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
    r=BeautifulSoup(requests.get(url,headers=headers).text)
    r.encoding = 'utf-8'
    html = r.text
    soup = BeautifulSoup(html[4550:])
    text = soup.get_text()
    clean_text= text.replace("\n"," ")
    clean_text= clean_text.replace("/", " ")       
    clean_text= ''.join([c for c in clean_text if c != "'"])
    return (clean_text[0:(len(clean_text)-1400)])


stop_words = stopWord()



cleaned_text = [readURL(i) for i in df_ip['URL']]
df_op['cleaned text'] = cleaned_text


preprocess_tag = [text_prep(i) for i in df_op['cleaned text']]
df_op["preprocess_txt"] = preprocess_tag

df_op['WORD COUNT'] = df_op['preprocess_txt'].map(lambda x: len(x))

charCount = [charCount(i) for i in df_op['cleaned text']]
df_op['Char Count'] = charCount

sentenceCount = [sentenceCount(i) for i in df_op['cleaned text']]
df_op['Sentence Count'] = sentenceCount

syl_cnt = [syllableCount(i) for i in df_op['cleaned text']]
df_op['Syllable Count'] = syl_cnt

com_word_cnt = [complexWord(i) for i in df_op['cleaned text']]
df_op['COMPLEX WORD COUNT'] = com_word_cnt

pcnt = [pronounCount(i) for i in df_op['cleaned text']]
df_op['PERSONAL PRONOUNS'] = pcnt

file = open('negative-words.txt', 'r')
neg_words = file.read().split()
file = open('positive-words.txt', 'r')
pos_words = file.read().split()

num_pos = df_op['preprocess_txt'].map(lambda x: len([i for i in x if i in pos_words]))
df_op['POSITIVE SCORE'] = num_pos

num_neg = df_op['preprocess_txt'].map(lambda x: len([i for i in x if i in neg_words]))
df_op['NEGATIVE SCORE'] = num_neg

df_op['POLARITY SCORE'] = (df_op['POSITIVE SCORE'] - df_op['NEGATIVE SCORE']) / (df_op['POSITIVE SCORE'] + df_op['NEGATIVE SCORE'] + 0.000001)

df_op['SUBJECTIVITY SCORE'] = (df_op['POSITIVE SCORE'] + df_op['NEGATIVE SCORE']) / (df_op['WORD COUNT'] + 0.000001 )

df_op['AVG SENTENCE LENGTH'] = df_op['WORD COUNT'] / df_op['Sentence Count']

df_op['PERCENTAGE OF COMPLEX WORDS'] = df_op['COMPLEX WORD COUNT'] / (df_op['WORD COUNT'] )

df_op['FOG INDEX'] = 0.4 * (df_op['AVG SENTENCE LENGTH'] + df_op['PERCENTAGE OF COMPLEX WORDS'])

df_op['AVG NUMBER OF WORDS PER SENTENCE'] = df_op['WORD COUNT'] / df_op['Sentence Count']

df_op['SYLLABLE PER WORD'] = df_op['Syllable Count'] / df_op['WORD COUNT']



df_op['AVG WORD LENGTH'] = df_op['Char Count'] / df_op['WORD COUNT']

df_op = df_op.drop('Char Count',axis=1)
df_op = df_op.drop('preprocess_txt',axis=1)
df_op = df_op.drop('Syllable Count',axis=1)
df_op = df_op.drop('Sentence Count',axis=1)
df_op = df_op.drop('cleaned text',axis=1)

df_op.to_excel("Output Data Structure.xlsx")


print(df_op)