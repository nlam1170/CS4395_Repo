import sys
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

'''
GUESSING GAME PORTION OF THE ASSIGNMENT BELOW

'''

#guess class to keep track of the state of user guess
class Guess:
    #intiially we set all the guess tokens to "_" since user has inputted no guesses yet
    def __init__(self, target_word):
        self.tokens = ["_" for _ in range(len(target_word))]
    #helper method to easily current current guess state to a string
    def to_str(self):
        return " ".join(self.tokens)

#the game class that handles all game logic and state
class GuessingGame:
    #the initializer, which stores the list of possible guess from our most common words
    #we set the score to an initial value of 5 per the rules
    #we set the target word to random word from the list of possible target words
    #we create a guess class instance using the target words
    #we create a set to keep track of guesses the user has already made
    def __init__(self, guess_list):
        self.guess_list = guess_list
        self.score = 5
        self.set_target_word()
        self.guess = Guess(self.target)
        self.already_guessed = set()

    #helper function to check if player score is too low
    def check_lose(self):
        return True if self.score < 0 else False

    #helper function to check if the player has guessed all letters correctly
    def check_win(self):
        return True if "_" not in self.guess.tokens else False

    #helper function to pick a random word from the list of possible target words
    def set_target_word(self):
        random_indx = random.randrange(len(self.guess_list))
        self.target = self.guess_list[random_indx]

    #main loop to play the game
    def start_game(self):
        print("Let's play a guessing game!\n")

        #infinite loop till player losses or wins
        while True:
            #print the current state of the user guess info
            print(self.guess.to_str())
            #get guess from user
            user_guess = self.get_user_guess()
            #call appropriate update logic for the guess
            self.check_guess(user_guess)

            #if player score is too low, print the loss statement and exit
            if self.score < 0:
                print("Sorry you lost!")
                print("Current score:", self.score)
                sys.exit()

            #if player has guessed the word, print the win statement and exit
            if self.check_win():
                print(self.guess.to_str())
                print("You solved it!")
                print("Current score:", self.score)
                sys.exit()

    #helper function to get the user guess from stdin
    def get_user_guess(self):
        guess = input("Guess a letter: ")
        return guess

    #helper function to update the state logic depending on users guess
    def check_guess(self, guess):
        #the auto forfeit symbol, ends the game
        if guess == "!":
            print("You have forfeited")
            print("Current score:", self.score)
            sys.exit()
        #check that the player has not guessed a letter they already guessed before
        if guess in self.already_guessed:
            print("You have already guessed that. Try again")
            return
        #add the guess to the already guessed list
        self.already_guessed.add(guess)
        #if the guess letter is in the target word, then update the guess object
        if guess in self.target:
            self.handle_correct_guess(guess)
        else:
            #if wrong letter, handle accordingly
            self.handle_wrong_guess()
    
    #helper function to update the game logic if guess is correct
    def handle_correct_guess(self, guess):
        #increment the score since guess is correct
        self.score += 1
        #print the correct guess statement
        print("Right! Score is", self.score)
        #loop through the guess object tokens and change them from "_" to the correct letter that the user guessed
        for i in range(len(self.target)):
            if self.target[i] == guess:
                self.guess.tokens[i] = guess
    
    #helper function to handle a wrong guess
    def handle_wrong_guess(self):
        self.score -= 1
        print("Sorry, guess again. Score is", self.score)

    #helper function to check if the user has won, or that there are no "_"  left in the guess object tokens
    def check_win(self):
        return False if "_" in self.guess.tokens else True

'''
FILE PARSING PORTION OF THE ASSIGNMENT BELOW

'''

#helper function to get the input file from stdin and preform some validation
def get_file():
    #if the user has not supplied a input file or has supplied more than one
    #we print an error and exit
    if len(sys.argv) != 2:
        print("Wrong number of arugements")
        sys.exit()
    
    #get the file name from stdin
    file_name = sys.argv[1]
    
    #the specified file could still be invalid for whatever reason,
    #so we try to open the file and return the file if it works, otherwise we print error
    #and exit the program if the file cannot be opened/read
    try:
        file = open(file_name)
    except Exception as e:
        print("Could not open/read", file_name)
        sys.exit()
    else:
        return file

#helper function to calculate the lexical diversity and print it
def calculate_lexical_diversity(tokens):
    diversity = len(set(tokens)) / len(tokens)
    print("The lexical diversity is: {:.2f}\n".format(diversity)) 

#helper function to parse the file text as specified
def parse_file(file):
    #read in all the file contents
    contents = file.read()
    #lowercase all contents
    contents = contents.lower()
    #tokenize the file contents with NLTK
    tokens = word_tokenize(contents)
    #print out the lexical diversity
    calculate_lexical_diversity(tokens)
    #get a set of the stop words in english using NLTK
    stop_words_set = set(stopwords.words("english"))
    #remve tokens that are not alpha, are shorter than 5 chars and in the stop words set
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words_set and len(t) > 5]
    
    #create the lemmatizer object class
    wnl = WordNetLemmatizer()
    #lemmatize all the tokens
    lemmas = [wnl.lemmatize(t) for t in tokens]
    #use a set to get all the unique lemmas
    lemmas = set(lemmas)
    #tag all the unique lemmas
    tags = nltk.pos_tag(lemmas)
    #print the first 20 tagged lemmas
    print("First 20 tagged words:", tags[:20], "\n")

    #get only the lemmas that are tagged as nouns
    noun_lemmas = [tag[0] for tag in tags if tag[1] == "NN"]
    #print info
    print("Length of tokens from step A:", len(tokens))
    print("Length of tokens from step D:", len(noun_lemmas), "\n")
    #return all the tokens, and the noun lemmas
    return tokens, noun_lemmas

#helper function to get a list of the 50 for most noun lemmas in all the tokens
def get_most_common_words(tokens, noun_lemmas):
    #create count dict
    count = {}
    #for each noun, count the occurence in the token and store to dict
    for noun in noun_lemmas:
        count[noun] = tokens.count(noun)
    #sort the dict from higher to lower by count value
    count = dict(sorted(count.items(), key = lambda item: item[1], reverse=True))
    #get the 50 words that have the highest occurence count
    most_common_words = list(count.items())[0:50]
    #print them
    print("The 50 most common words and their count:", most_common_words, "\n")
    #return only the common words, excluding the count
    return [w[0] for w in most_common_words]

#program run function
def main():
    #get file from user
    file = get_file()
    #parse the file to get the tokens, and nouns
    tokens, noun_lemmas = parse_file(file)
    #use the tokens and nons to get most common words
    most_common_words = get_most_common_words(tokens, noun_lemmas)
    #create game object, passing in the most common words as the possible guess list
    game = GuessingGame(most_common_words)
    #play the game
    game.start_game()



if __name__ == "__main__":
    main()

