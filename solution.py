###############################################################
# New units (lists) for diagonal sudoku constraints
###############################################################
diagonal1 = ["A1", "B2", "C3", "D4", "E5", "F6", "G7", "H8", "I9"]
diagonal2 = ["I1", "H2", "G3", "F4", "E5", "D6", "C7", "B8", "A9"]
diagonal_units = []
diagonal_units.append(diagonal1)
diagonal_units.append(diagonal2)



assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# updated unitlist  - added diagonal_units
unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)




###############################################################
# New method
# 
# find_twins
###############################################################
def find_twins(values, unit):
    """
    Args:
        values: a dictionary of the form {'box_name': '123456789', ...}
        unit: list of 9 boxes comprising the unit 
        
    Returns:
        list of naked twins (i.e. ["23", "58"])
    
    Logic:
        We know that if we find exactly 2 boxes with the same 2-digit
        value, we have a naked twin. We first get a count of the 2 digit
        values. Then we create and return a list where the count is 2.
        
        We only need the actual twin values and not the box names.
        
        And yes, there may be more compact Python code to perform this
        function, but this is readable and maintainable.
    """
    # count of all two-digit values
    counts = {}
    for u in unit:
        v = values[u]
        if (len(v)==2):
            if (v not in counts):
                counts[v] = 1
            else:
                counts[v] = counts[v] + 1    
    
    # return list of naked twins
    ret = []
    for digits, cnt in counts.items():
        if (cnt==2):
            ret.append(digits)
    
    return ret

###############################################################
# New method
#
# remove twin digits
###############################################################
def remove_twin_digits(values, twin_list, this_unit):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        twin_list: list of twins (i.e. ["23", "58"])
        this_unit: list of 9 boxes comprising the unit 

    Returns:
        the values dictionary with the naked twins eliminated from peers.
        
    Logic: 
        For each twin, loop through the digits, removing each from the 
        peers. Of course, we do not touch the boxes containing the
        naked twins. 
    """     
    for twin in twin_list:
        for digit in twin:
            for box in this_unit:
                boxvalue = values[box]
                if (twin!=boxvalue and digit in boxvalue):
                    oldvalue = boxvalue
                    values = assign_value(values, box, values[box].replace(digit,""))
                    #display(values)
                    print("twin=" + twin + " removing digit=" + digit + " from " + box + " old value=" + oldvalue + "  updated value=" + values[box])
    return values


###############################################################
# Provided method
#
###############################################################
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

###############################################################
# New code
#
# naked_twins
###############################################################
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
        
    Logic: 
        Naked twins exist when two boxes contain two digits, and those 
        two digits are the same. When we find naked twins, we can remove
        those digits from all peers in the unit.
        
        For each of the units, we find all the naked twins then remove 
        those digits from the peers. 
    """     
    for this_unit in unitlist:
        twin_list = find_twins(values, this_unit) 
        values = remove_twin_digits(values, twin_list, this_unit) 
    return values

###############################################################
# Provided code from the class
#
###############################################################   
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

###############################################################
# Provided code from the class
#
###############################################################
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

###############################################################
# Provided code from the class
#
###############################################################
def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

###############################################################
# Provided code from the class
#
###############################################################
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

###############################################################
# Provided code from the class,
# updated with the naked_twins() call
#
###############################################################
def reduce_puzzle(values):
    #solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = naked_twins(values)
        values = eliminate(values)
        values = only_choice(values)
        
        
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

###############################################################
# Provided code from the class
#
###############################################################
def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

###############################################################
# Provided code
#
###############################################################
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
