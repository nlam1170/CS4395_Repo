import sys
import re
import pickle

#Person class object to easier store the differnt info about a person
class Person:
    #initializer method
    def __init__(self, last, first, middle, id, phone):
        self.last = last
        self.first = first
        self.middle = middle
        self.id = id
        self.phone = phone
    
    #method to print print the person information according to the specified standards
    def display(self):
        print("Employee id:", self.id)
        print("\t"+self.first, self.middle, self.last)
        print("\t"+self.phone)

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

#helper function to validate the id using regex, if the id is invalid we continously prompt
#the user to enter a valid id, till they do
def parse_id(id):
    #regex pattern to use for matching, any two letters followed by 4 digits only
    pattern = re.compile(r"[a-zA-Z]{2}\d{4}$")
    #while the specified id does not match the pattern, prompt the user for the correct id
    while not pattern.match(id):
        print("ID invalid:", id)
        print("ID is two valid letters followed by 4 digits")
        id = input("Please enter a valid id: ")
    #since we only reach here, if id is valid, return id
    return id

#helper function to validate the phone number using regex, if the phone number is invalid
#we continously prompt the user to enter a valid phone number till they do
def parse_phone(phone):
    #regex pattern to use for matching, in the form 123-456-7890
    pattern = re.compile(r"\d{3}-\d{3}-\d{4}$")
    #while the specified phone does not match the pattern, prompt the user for the correct
    #phone number
    while not pattern.match(phone):
        print("Phone", phone, "is invalid")
        print("Enter phone number in form 123-456-7890")
        phone = input("Enter phone number: ")
    #since we only reach here if phone is valid, return phone
    return phone

#helper function to parse each line of the file
def parse_file(file):
    #store each line as an item in list
    lines = file.readlines()
    #initialize the persons dict, that we return after filling it with valid info
    persons = {}

    #iterate through each line in the file, skipping the first one since its just the headers
    for line in lines[1:]:
        #split each line by "," since its CSV format
        line = line.split(",")
        #get the first name and capitalize it
        last = line[0].capitalize()
        #get the last name and capitalize it
        first = line[1].capitalize()
        #no middle name might exist so just return X otherwise get capitalize middle initial
        middle = "X" if len(line) == "" else line[2].upper()
        #get the id, using the hlper function for validation and input
        id = parse_id(line[3])
        #get the phone number using the helper function for validationa and input
        phone = parse_phone(line[4])

        #create a person object with all the valid info
        person = Person(last, first, middle, id, phone)
        #if duplicate id found, print an error and exit, otherwise add the person to the dictionary
        #using the id as the key
        if id in persons:
            print("ERROR: duplicate id found")
            sys.exit()
        else:
            persons[id] = person
    #return the persons dictionary
    return persons

#main function to execute all logic        
def main():
    #get file object
    file = get_file();
    #create persons info dict from file object
    persons_dict = parse_file(file)
    #dump our persons info to pickle file
    pickle.dump(persons_dict, open("persons.p", "wb"))
    #serialize it back into a new python dictionary
    persons_dict_in = pickle.load(open("persons.p", "rb"))

    #easily print all employee information using the display method
    print("\n\nEmployee list:\n")
    for key in persons_dict_in:
        persons_dict_in[key].display()


if __name__ == "__main__":
    main()
