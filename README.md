# CS4395 - Intro To NLP

[Link to this page](https://nlam1170.github.io/CS4395_Repo)

## NLP Overview Assignment
My answers to the assignment can be viewed [here](nlp_overview_assignment.pdf)

## Assignment 1
My code for the assignment can be viewed [here](https://github.com/nlam1170/CS4395_Repo/blob/main/Assignment1/run.py)

### Program Description
The program reads in a data file containing different information about employees. It performs some validation on the file, such as checking for a valid ID format, and prompting the user to enter the correct ID if the ID is found to be invalid. It then creates a dictionary object containing different Person classes for each employee in the input file. That dictionary is then serialize into a pickle file, then deserialize back by python and prety printed

### How To Run
The file can be run using a standard python intrepretor, and then passing in an input file arg.

Example:\
`python3 run.py data.csv`

### Python for text procesing
Python is very nice in that it is very easy to start writing code and have a working program in a small amount of time. The Regex and file API's were also very easy to work with and be productive. However, fixing bugs was very tedious since there are no types and compile time checks. I had to keep manually running the programming and waiting for it not to crash at runtime. Error handling is also subpar, since there is no explicit need to take action on error, and the error information that python provides is not great.

### What I Learned
I have been using python for quite a while, so I was familiar how to do most of the tasks for this assignment. However I did learn how to use the regex library better, since regex is something that I mostly try to avoid for my personal use. I also learned how to use the pickle library and format. This is a format that I have never worked with in the past, so that was useful as well. The other python related tasks such as classes and working with files was still a good review for me.

## Assignment 2
My code for this assignment can be viewed [here](https://github.com/nlam1170/CS4395_Repo/blob/main/Assignment2/assignment2.ipynb)

The rendered PDF for this assignment can be viewed [here](https://github.com/nlam1170/CS4395_Repo/blob/main/Assignment2/assignment2.pdf)

## Assignment 3
My code for this assignment can be viewed [here](https://github.com/nlam1170/CS4395_Repo/blob/main/Assignment3/run.py)

### How To Run
An input file should be specified like below.

Example:\
`python3 run.py anat19.txt`
