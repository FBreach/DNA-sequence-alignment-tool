DNA Sequence Alignment Tool

This Python script performs optimal DNA sequence alignment using dynamic programming. The script calculates the best possible alignment between two DNA sequences by considering match scores, mismatch penalties, and gap penalties.



Features:

• 	Dynamic Scoring Matrix: Utilizes a dynamic programming matrix to calculate the optimal alignment scores.

• 	Backtracking for Alignment: Determines the best alignment path by backtracking through the scoring matrix.

•	Efficient Computations: Optimized with NumPy for efficient array operations and designed to minimize computational overhead.



Requirements:

•	Python 3.x

•	NumPy

•	Numba

Ensure that you have the latest version of Python and the required packages installed. You can install NumPy and Numba using pip:




Usage:

The script reads two DNA sequences from files, aligns them, and prints the optimal alignment along with its score and the time taken for the computation.

 1.	Prepare two text files, each containing a DNA sequence. The files should contain only the sequence letters (A, C, G, T).

 2.	Run the script from the command line, providing the paths to the sequence files as arguments:

python dna_alignment.py path_to_sequence1.txt path_to_sequence2.txt 



Example Files:

 •	sequence1.txt: Contains the DNA sequence for sequence1.

 •	sequence2.txt: Contains the DNA sequence for sequence2.

Ensure that these files are in the same directory as the script or provide the full path.



Output:

The script will display:

 •	The alignment of the two sequences.

 •	A line showing matches with | and mismatches with spaces.

 •	The total alignment score.

 •	The computation time.
