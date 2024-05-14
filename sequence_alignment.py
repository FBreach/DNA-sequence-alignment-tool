#!/usr/bin/python
import time
import sys
import numpy as np
from numba import jit, int32


seq1 = "AGGATAGA"
seq2 = "CTGAGGAT"



# YOUR FUNCTIONS GO HERE -------------------------------------
# 1. Populate the scoring matrix and the backtracking matrix

# ------------------------------------------------------------

# FOR GREATEST EFFICIENCY RUN IN PYTHON 2.7!!!!! It has a smaller integer value, whereas python
# 2.x x>7 has only a very long integer value for storing so is therefore more efficient for this
# application.

scores_dict = {'A': 4, 'C': 3, 'G': 2, 'T': 1}

# @profile
def scoring():
    # global scores_dict
    top = len(seq1) + 1
    side = len(seq2) + 1
    bt = np.zeros((side, top), dtype=np.str_)  # The backtracking matrix
    s1 = np.array(list(seq1), dtype=np.str_)  # Seq1 as a numpy array for efficiency in np.where,
    # only done once instead of in loop

    v = np.array(range(0, top * -2, -2), dtype=np.int_)  # A list of values for the row above,
    # initially ascending gaps score

    bt[0, 1:] = 'L'  # Setting backtracking matrix to L and U for the first row and column
    bt[1:, 0] = 'U'
    # scores_dict = {'A': 4, 'C': 3, 'G': 2, 'T': 1}  # A dictionary of the scores for if there is
    # a match
    directions = []
    for i in range(1, side):
        t = seq2[i-1]  # t is the letter of seq2 which is the row in backtracking matrix
        val = scores_dict[t]  # val is the score of a match if they match

        diagonals = np.where(s1 != t, -3, val) + v[:-1]  # np.where will iterate through s1 and
        # where the condition s!= t is true it will give the value -3, a mismatch, and where it
        # isn't true it gives the score set by val above.
        ups = v[1:] - 2  # getting the score up Up - 2, using numpy broadcasting for efficiency
        # so it is only
        # calculated in one for loop
        directions = np.where(diagonals >= ups, 'D', 'U')  # Getting a matrix of D or U depending
        # on which value from diagonals and ups is greater. This eliminates a need for three if
        # statements to see which is greater of Up Diagonal and Left in a second for loop,
        # cutting down computation massively.
        v = np.where(diagonals >= ups, diagonals, ups).tolist()  # v is now an array doing the
        # same comparison as above, but for numeric values. It is overwriting v which means there
        # are fewer variables needed overall, however it isn't an operation that is done in
        # place, but is converted to a list so that the next bit is more efficient
        v.insert(0, -2*i)  # Done in python list as it is far quicker, it simulates the values of
        # the gaps on the vertical side of the scoring matrix

        for j in range(top - 1):
            left = v[j] - 2  # Calculates the value of Left
            if v[j+1] < left:  # If left is greater than the value of v (the greater of U and D)
                # then:
                directions[j] = 'L'  # update directions to be L
                v[j+1] = left  # and values to be the value of L

        """
            This whole second for loop has been optimised to do as fewer calculations as 
            possible. There is one value calculation, and one if statement, which a lot of the 
            time doesn't return true. Inside this if statement there is then only 2 further 
            operations which are just assigning values to certain arrays. If it doesn't return 
            true then we know the array must already hold the greatest value and the most optimum
            direction.
        """

        v = np.array(v)  # make v a numpy array again for efficiency in the loop
        bt[i, 1:] = directions  # Make the backtracking matrix be the array of directions.
    return route(bt, side - 1, top - 1, directions[-1])


# @profile
# This is pretty self explanatory, it backtracks through the direction matrix
def route(back, i, j, loc):
    if loc == 'D':
        i -= 1
        j -= 1
        ans1 = seq1[j]
        ans2 = seq2[i]
    elif loc == 'L':
        j -= 1
        ans1 = seq1[j]
        ans2 = '-'
    else:
        i -= 1
        ans1 = '-'
        ans2 = seq2[i]
    loc = back[i][j]
    while loc != '':
        if loc == 'D':
            i -= 1
            j -= 1
            ans1 = seq1[j] + ans1
            ans2 = seq2[i] + ans2
            loc = back[i][j]
        elif loc == 'L':
            j -= 1
            ans1 = seq1[j] + ans1
            ans2 = '-' + ans2
            loc = back[i][j]
        else:
            i -= 1
            ans1 = '-' + ans1
            ans2 = seq2[i] + ans2
            loc = back[i][j]
    return [ans1, ans2]


# @profile
# A function to return the best score. It is quicker to sum all the (mis)match/gap scores of best
# alignment than it is to retrieve the value in the last place of the scoring matrix.
def finale(i):
    thing = best_alignment[0][i]
    if thing == '-' or best_alignment[1][i] == '-':
        return -2
    elif thing != best_alignment[1][i]:
        return -3
    else:
        return scores_dict[thing]
        # if thing == 'A':
        #     return 4
        # elif thing == 'C':
        #     return 3
        # elif thing == 'G':
        #     return 2
        # else:
        #     return 1


# DO NOT EDIT ------------------------------------------------
# Given an alignment, which is two strings, display it

def displayAlignment(alignment):
    string1 = alignment[0]
    string2 = alignment[1]
    string3 = ''
    for i in range(min(len(string1),len(string2))):
        if string1[i]==string2[i]:
            string3=string3+"|"
        else:
            string3=string3+" "
    print('Alignment ')
    print('String1: '+string1)
    print('         '+string3)
    print('String2: '+string2+'\n\n')

# ------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This opens the files, loads the sequences and starts the timer
file1 = open(sys.argv[1], 'r')
seq1=file1.read()
file1.close()
file2 = open(sys.argv[2], 'r')
seq2=file2.read()
file2.close()
start = time.time()

# -------------------------------------------------------------


# YOUR CODE GOES HERE ----------------------------------------
# The sequences are contained in the variables seq1 and seq2 from the code above.
# Intialise the scoring matrix and backtracking matrix and call the function to populate them
# Use the backtracking matrix to find the optimal alignment
# To work with the printing functions below the best alignment should be called best_alignment
# and its score should be called best_score.

best_alignment = scoring()
best_score = sum([finale(x) for x in range(len(best_alignment[0]))])

# -------------------------------------------------------------


# DO NOT EDIT (unless you want to turn off displaying alignments for large sequences)---------------
# This calculates the time taken and will print out useful information
stop = time.time()
time_taken=stop-start

# Print out the best
print('Time taken: '+str(time_taken))
print('Best (score '+str(best_score)+'):')
displayAlignment(best_alignment)

# -------------------------------------------------------------
