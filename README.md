# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: When we have naked twins (two boxes with the same two values), we can
introduce new contraints on other boxes in the unit. We remove the naked twin
digits from the other boxes in the same unit, reducing the possible solutions
for those boxes.

I think the question is backward. My understanding is that we aren't really 
solving the naked twins problem, but rather we recognize when
naked twins exist and use them to propagate contraints (remove digits) 
from the other boxes.  We then assume that another contraint will reduce the two
naked twins boxes to one digit each. Naked twins are not a problem - they are part of
the solution. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: A diagonal sudoku is a regular sudoku with the added rule that the two
diagonals (9 boxes each) are also considered to be units. The diagonals follow
the same "9 unique digits" rule. These diagonals add more contraints to
those diagonal boxes. 

Adding the diagonal rules to the existing code was a simple exercise of 
defining the two diagonal units and adding them to the "unitlist". The 
"unitlist" values get propagated to "units" and "peers" and are then used
by the existing methods.






### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.