#library imports
import sys
import pickle
from nltk import word_tokenize
from nltk.util import ngrams

#return a list of unigram from tokens
def create_unigram(tokens):
    return list(ngrams(tokens, 1))

#return a list of bigram tuples from tokens
def create_bigram(tokens):
    return list(ngrams(tokens, 2))

#function to open input file and generate the proper unigram and bigrams
def make_ngrams(file_name):
    #try to open input file, return error msg and exit if problem exists
    try:
        file = open(file_name)
    except Exception as e:
        print("Could not open/read file", file_name)
        sys.exit()

    #read in all file contents
    content = file.read()
    #remove all newlines
    content = content.strip()
    #tokenzie the text
    tokens = word_tokenize(content)
    #generate the unigram from tokens
    unigram = create_unigram(tokens)
    #generate the bigram from tokens
    bigram = create_bigram(tokens)

    #make a unigram map to store unigram -> unigram count
    unigram_dict = {}
    for u in unigram:
        unigram_dict[u[0]] = 1 + unigram_dict.get(u[0], 0)

    #make a bigram map to store bigram(word, word) -> count
    bigram_dict = {}
    for b in bigram:
        bigram_dict[b] = 1 + bigram_dict.get(b, 0)

    #return the two count dictionaries
    return unigram_dict, bigram_dict


if __name__ == "__main__":
    #languages for our input files
    languages = ["English", "French", "Italian"]

    #for each input language, generate the unigram and bigram and save to a pickle file
    for language in languages:
        unigram, bigram = make_ngrams(f"testfiles/LangId.train.{language}")
        pickle.dump(unigram, open(f"outputfiles/unigram_{language.lower()}.p", "wb"))
        pickle.dump(unigram, open(f"outputfiles/bigram_{language.lower()}.p", "wb"))





