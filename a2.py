"""
===========================
A2
Puzzzle Solver

Victor Soledad
===========================
"""
print(__doc__)

import sys
import numpy
from a2_functions import *

sys.setrecursionlimit(2100000000)


if __name__ == '__main__':
    
    pformat = [2,4]

    puzzledata = generatePuzzles(pformat, 50)
    # puzzledata = puzzleParser("samplePuzzles.txt", pformat)
    puzzledata = puzzleParser("randomPuzzles.txt", pformat)


    xsolutionsUCS = []
    xsolutionsGBFS1 = []
    xsolutionsGBFS2 = []
    xsolutionsAS1 = []
    xsolutionsAS2 = []

    pcount = 0
    for puzzle in puzzledata:
        printPuzzle(puzzle, pformat, True)


        xsolutionsUCS.append( puzzleSolver(puzzle, "UCS",  0, pformat, pcount) )
        xsolutionsGBFS1.append( puzzleSolver(puzzle, "GBFS", 1, pformat, pcount) )
        xsolutionsGBFS2.append( puzzleSolver(puzzle, "GBFS", 2, pformat, pcount) )
        xsolutionsAS1.append( puzzleSolver(puzzle, "A*",   1, pformat, pcount) )
        xsolutionsAS2.append( puzzleSolver(puzzle, "A*",   2, pformat, pcount) )


        pcount += 1

    analizeSolutions("ucs", xsolutionsUCS)
    analizeSolutions("gbfs-h1", xsolutionsGBFS1)
    analizeSolutions("gbfs-h2", xsolutionsGBFS2)
    analizeSolutions("astar-h1", xsolutionsAS1)
    analizeSolutions("astar-h2", xsolutionsAS2)
