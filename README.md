# Project Description
This project was made for CSPC 481 at CSUF - Artificial Intelligence. Where we had to create an AI based on what we have learned in the course. The current AI algorithim is Depth-First Search. Code for the game and AI is under sudokuGame.py

## Installation
Every library used should already be included with Python's Standard Library. 

## Usage
```bash
python3 main.py --board [boardfile.txt] --variant [varient name]
```

**A board must be included**

Board files must have 9 lines with each line being 9 characters long an example of this is shown here:
```
089040672
600782195
752000840
906400320
030208569
005630010
094000736
061375984
070900051
```
**Variants are optional**

The current variant types are:
* diagonal
* king
* knight
* chess

## Roadmap

In no particular order:
* Add a GUI
* Add forward checking
* Improve the AI with other Sudoku Checking techniques
