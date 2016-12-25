# Jeopardy in Python
I had seen some jeopardy games prepared with Powerpoint slides to use in the classroom but the problem was keeping track of the game as in which questions had already been answered and what the scores were.
This is a simple implementation of the jeopardy game using python. The purpose of this game is to be able to create fast content for the class room and use the jeopardy game as an activity to teach in the classroom with more engament among the students. The questions are stored in CSV file (editable with any spreadsheet application). 
The rows begin from one since row 0 is dedicated to categories stored under the categories section in the CSV file.

| Row | Col | Question      | Answer | Categories
| --- |:---:| -------------:|-------:|-----------:|
| 1   | 0   | Some Question | ANS    | CAT 0      |


This method can be used in the classroom for any subject and as tool for review or teaching new material.

## Prerequisites:
You need to have python3 installed and also to either clone this repository or have the files in the repo in a directory.

## How to use:
simply create an excel file as in the repository for your question set.
Navigate to the directory with the jeopardy.py file
```shell
# python3 jeopardy.py
```
Answer the questions from the promptas to how many teams and team names and you are set to go.
