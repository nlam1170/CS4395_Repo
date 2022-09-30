#library imports
import pickle
import sys
from nltk import word_tokenize
from nltk.util import ngrams

#read in the unigram and bigrams from the pickle files and store it in a master dictionary
def load_ngrams():
    ngrams = {}
    languages = ["english", "french", "italian"]

    for language in languages:
        unigram_file = f"outputfiles/unigram_{language}.p"
        bigram_file = f"outputfiles/bigram_{language}.p"

        #read in unigram and bigram from file
        unigram = pickle.load(open(unigram_file, "rb"))
        bigram = pickle.load(open(bigram_file, "rb"))
        
        #store in a map using the language and either unigram or bigram as keys
        ngrams[language] = {
            "unigram": unigram,
            "bigram": bigram,
        }
    #return map
    return ngrams

#gets a list of the test file lines, returns error if cant access file properly
def get_test_lines(file_name):
    try:
        test_file = open(file_name)
    except Exception as e:
        print("Could not open/read file", file_name)
        sys.exit()

    lines = test_file.readlines()
    return lines

#helper function to calculate the probability for a single test_bigram
def calculate_prob(bigram, unigram, total_vocab_count, test_bigram):
    return (bigram.get(test_bigram, 0) + 1) / (unigram.get(test_bigram[0], 0) + total_vocab_count)

#function to test all the bigrams of a single line, and return the guess language
def test(line, all_ngrams, total_vocab_count):
    #tokenzie the line
    tokens = word_tokenize(line)
    #generate bigrams from the lines
    bigrams = list(ngrams(tokens, 2))
    english_prob, french_prob, italian_prob = 1, 1, 1

    #for each bigram from the line, calculate the probability for all three languages
    for b in bigrams:
        english_prob *= calculate_prob(all_ngrams["english"]["bigram"], all_ngrams["english"]["unigram"], total_vocab_count, b)
        french_prob *= calculate_prob(all_ngrams["french"]["bigram"], all_ngrams["french"]["unigram"], total_vocab_count, b)
        italian_prob *= calculate_prob(all_ngrams["italian"]["bigram"], all_ngrams["italian"]["unigram"], total_vocab_count, b)

    #get the max probability
    max_prob = max(english_prob, french_prob, italian_prob)

    #return the language that the max_probability corresponds to
    if max_prob == english_prob:
        return "English"
    elif max_prob == french_prob:
        return "French"
    else:
        return "Italian"
        
#run the test function on all lines in the input file
def run_test(file_name):
    #load the the unigram and bigram for all three languages
    all_ngrams = load_ngrams()
    #get the total vocab count
    total_vocab_count = len(all_ngrams["english"]["unigram"]) + len(all_ngrams["french"]["unigram"]) + len(all_ngrams["italian"]["unigram"])
    #get the list of test lines
    test_lines = get_test_lines(file_name)
    #open file to write out guesses to
    output_file = open("outputfiles/LangId.test_output", "w+")

    #make a guess and write to the file
    line_num = 1
    for line in test_lines:
        guessed_lang = test(line, all_ngrams, total_vocab_count)
        output_file.write(f"{line_num} {guessed_lang}\n")
        line_num += 1

#function to output some stats to stdout
def output_stats(output_file, solution_file):
    #open the file that we wrote out guesses too and the file that contains the actaul answers
    try:
        output = open(output_file)
        solution = open(solution_file)
    except Exception as e:
        print("Could not open/read file")
        sys.exit()

    #read the llines for each file into a list
    output_lines = output.readlines()
    solution_lines = solution.readlines()
    #list to store the line numbers for the guess we got wrong
    incorrectly_classified = []
    #count vars for the langugages that we guessed right
    english_correct, french_correct, italian_correct = 0, 0, 0
    #counter var that we incremement for each comparasin
    total_checks = 0

    #get the corresponding line for our guess and correct solution
    for out_line, sol_line in zip(output_lines, solution_lines):
        #split the solution into line number and answer language
        sol_split = sol_line.split()
        #increment the check ount
        total_checks += 1

        #if our guess matches the solution, increment the language correct counter
        if out_line == sol_line:
            if sol_split[1] == "English":
                english_correct += 1
            elif sol_split[1] == "French":
                french_correct += 1
            else:
               italian_correct += 1
        #if wrong guess, then append to our incorrectly classified list
        else:
            incorrectly_classified.append(int(sol_split[0]))

    #print statistics
    print("Accuracy for Correct Classifications:\n")
    print(f"English: {english_correct/total_checks*100}%")
    print(f"French: {french_correct/total_checks*100}%")
    print(f"Italian: {italian_correct/total_checks*100}%")
    print("\nLine numbers for Incorrect Classifications:\n")
    print(incorrectly_classified)


if __name__ == "__main__":
    #run function to generate our guess
    run_test("testfiles/LangId.test")
    #use our guess, and the solution file to output stats
    output_stats("outputfiles/LangId.test_output", "testfiles/LangId.sol")