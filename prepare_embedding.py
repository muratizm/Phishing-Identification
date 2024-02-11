import os
import sys
import trafilatura
from sentence_transformers import SentenceTransformer
import numpy as np
from googletrans import Translator
import pickle
import time

def parse_html_file(directory_path):
    extracted_htmls = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html = file.read()
        except:
            with open(file_path, 'r', encoding='windows-1252') as file: #some html.txt files was saved with encoding windows-1252 but most with utf-8
                html = file.read()
        extracted_htmls.append(trafilatura.extract(html))
    return np.array(extracted_htmls)


def translate_to_english(arr):
    #this part gave lots of errors such as too many request, timeout errors due to google translate api and being poor :/
    #when translating we had to run seperate times with subslicing the arr, but since it dont look pretty we decided to put it like this
    #theoreticly this works depending on the good day of google translate, but on practice since we can't buy 200$ developer pack we changed our ip frequently with vpn to not get too many request error
    #hopefully you will consider this while running :) have a great day!
    translator = Translator()
    max_chars = 4900 # there is a char limit to translate which is 5000 but to make sure we've set it to 4900
    translated_parts=[]
    long_parts = [part for part in arr if len(part) > max_chars]
    short_parts = [part for part in arr if len(part) <= max_chars]

    for i, part in enumerate(short_parts):
        try:
            translated_parts.append(translator.translate(part).text)
            time.sleep(0.1) # to not get too many requests error
            if ((i + 1) % 200 == 0):
                translator = Translator() # to not get too many requests error
        except Exception as e:
            print(f"Error: {e}")
            continue
    for i, part in enumerate(long_parts):
        try:
            chunks = [part[j:j + max_chars] for j in range(0, len(part), max_chars)]
            translated_text = ' '.join([translator.translate(chunk, dest='en').text for chunk in chunks])
            translated_parts.append(translated_text)
            time.sleep(0.5) # to not get too many requests error
            if ((i + 1) % 200 == 0):
                translator = Translator() # to not get too many requests error
        except Exception as e:
            print(f"Error: {e}")
            continue
    return np.array(translated_parts)

algorithm = sys.argv[1]

if not os.path.exists("embeddings"):
    os.makedirs("embeddings")

legit = parse_html_file("Legitimate")
legit = np.unique(legit[legit != None])
phish = parse_html_file("Phishing")
phish = np.unique(phish[phish != None])

name=""

if 'sbert' in algorithm or 'electra' in algorithm:
    legit=translate_to_english(legit)
    phish=translate_to_english(phish)

if 'xlm-roberta' in algorithm:
    model = SentenceTransformer("aditeyabaral/sentencetransformer-xlm-roberta-base",device="cuda")
    name="xlm-roberta"

elif 'sbert' in algorithm:
    model = SentenceTransformer("sentence-transformers/bert-base-nli-mean-tokens",device="cuda")
    name="sbert"

elif 'electra' in algorithm:
    model = SentenceTransformer("google/electra-small-discriminator",device="cuda")
    name="electra"

else:
    print("error")
    exit(0)

legitimate_data = model.encode(legit)
phishing_data = model.encode(phish)

legitimate_labels = np.zeros(len(legitimate_data))
phishing_labels = np.ones(len(phishing_data))

embedding_data = {
    'data': np.concatenate((legitimate_data, phishing_data), axis=0),
    'labels': np.concatenate((legitimate_labels, phishing_labels), axis=0)
    }

with open("embeddings/embedding-"+name+".pkl", 'wb') as f:
    pickle.dump(embedding_data, f)
