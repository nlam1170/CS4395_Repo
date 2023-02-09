import numpy as np
import random
import string
import requests
import random 
from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.filterwarnings("ignore")

import nltk
from nltk.stem import WordNetLemmatizer
#nltk.download("popular")
#nltk.download('punkt')
#nltk.download('wordnet')

URLS = [
        "https://en.wikipedia.org/wiki/Tiger",
        "https://www.britannica.com/animal/tiger",
        "https://kids.nationalgeographic.com/animals/mammals/facts/tiger",
        "https://www.worldwildlife.org/species/tiger",
        "https://www.livescience.com/27441-tigers.html",
        "https://a-z-animals.com/animals/tiger/",
        "https://nationalzoo.si.edu/animals/tiger",
        "https://www.theanimalfiles.com/mammals/carnivores/tiger.html",
        "https://awionline.org/content/tigers",
        "https://worldanimalfoundation.org/advocate/wild-animals/params/post/1297938/tigers",
        "https://www.animalfactsencyclopedia.com/Tiger-facts.html",
        "https://animalia.bio/tiger",
        "https://animals.fandom.com/wiki/Tiger"
    ]

def generate_corpus():
    for i in range(len(URLS)):
        url = URLS[i]
        res = requests.get(url)
        soup = BeautifulSoup(res.text, features="lxml")
        text = ""

        for paragraph in soup.find_all("p"):
            text += paragraph.get_text()

        try:
            f = open(f"corpus{i+1}.txt", "x")
            f.write(text)
        except:
            continue

def read_corpus():
    raw = ""

    for i in range(len(URLS)):
        f = open(f"corpus{i+1}.txt", "r", encoding="utf-8", errors="ignore")
        raw += f.read().lower()
    return raw

generate_corpus()
raw = read_corpus()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = WordNetLemmatizer()

def lem_tokens(tokens):
     return [lemmer.lemmatize(token) for token in tokens]

def lem_normalize(text):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "Im so happy you're talking to me!"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    robo_response = ""
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=lem_normalize, stop_words="english")
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response



print("TigerBot: Hello! my name is TigerBot. I will answer your queries about tigers. What is your name?")
user_name = input("\n>")

print(f"Hi {user_name}! nice to meet you. I love tigers! what do you like?")

likes_input = input("\n>")
likes_tokens = nltk.word_tokenize(likes_input)
likes_tag = nltk.pos_tag(likes_tokens)
likes = [word for word,pos in likes_tag if (pos == 'NN' or pos == "VB")]

print(f"Awesome I also like {random.choice(likes)}, but I really dislike poachers! What things do you dislike?")

dislikes_input = input("\n>")
dislikes_tokens = nltk.word_tokenize(dislikes_input)
dislikes_tag = nltk.pos_tag(dislikes_tokens)
dislikes = [word for word,pos in dislikes_tag if (pos == 'NN' or pos == "VB")]

print(f"I also hate {random.choice(dislikes)}!")

print(f"\n{user_name} do you have any questions about tigers?! You can always say \"bye\" to leave")


flag=True
while(flag==True):
    user_response = input("\n>")
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("\nTigerBot: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("\nTigerBot: "+greeting(user_response))
            else:
                print("\nTigerBot: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("\nTigerBot: Bye! take care..")  