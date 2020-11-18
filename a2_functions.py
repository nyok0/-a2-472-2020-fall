import numpy
import time
import random

import multiprocessing
import time

def puzzleParser(puzzlefile, pformat):
    file = open(puzzlefile, "r")
    xrow = []
    height, width = pformat
    for line in file:
        if(line[0] == "#"):
            continue
        newpuzzle = line.rstrip('\n').split(' ')

        if(len(newpuzzle) < height * width):
            for i in range( height * width - len(newpuzzle)):
                newpuzzle.append("O")

        if newpuzzle.count("0") > 1:
            print("Invalid Puzzle: More than one Zero Tile [" + line + "]")
            continue
        if "0" not in newpuzzle:
            print("Invalid Puzzle: Missing Zero Tile [" + line + "]")
            continue

        xrow.append(newpuzzle)
    file.close()
    return xrow

def printPuzzle(pdata, pformat, printHeader=False, xHeader=""):
    xcount = 0
    height, width = pformat
    plen = 1
    if(height * width >= 10):
        plen = 2
    if(height * width >= 100):
        plen = 3

    # plen = 20

    if(printHeader):
        print("===============")
        print("Puzzle " + str(height) + " x " + str(width))
    if(xHeader != ""):
        print("-------------")
        print(xHeader)
    for i in range(width * 2 + 3):
        print("-", end ="")
    print("")
    print("|", end =" ")
    for e in pdata:
        if(e == "0"):
            e = " "
            print(f"{e:>{plen}s}", end =" ")
        else:
            print(f"{e:>{plen}s}", end =" ")
            # print( '{0: <{plen}}'.format(e), end =" ")
        xcount += 1
        if(xcount % width == 0 and xcount < (height * width)):
            print("|")
            print("|", end =" ")
    print("|")
    for i in range(width * 2 + 3):
        print("-", end ="")
    print("")

def getNewPos(pdata, blankPos, newPos):
    ndata = pdata.copy()
    ndata[blankPos] = ndata[newPos]
    ndata[newPos] = "0"
    return ndata
    
def getPosibleMoves(pdata, pformat):
    wloc = [-1,-1]
    wind = -1
    xcount = 0
    ycount = 0
    height, width = pformat
    # Get White Location
    for e in pdata:
        if(e == "0"):
            wloc = [(xcount % width), (ycount)]
            wind = xcount
            break
        if((xcount + 1) % width == 0):
            ycount += 1
        xcount += 1
    if(wind == -1):
        return
    
    wres = []

    # CALCULATE LEFT MOVES
    if(wloc[0] > 0):
        ndata = getNewPos(pdata, wind, wind - 1)
        wres.append( [ndata, 1, "LEFT", ndata[wind]])

    # CALCULATE RIGHT MOVES
    if(wloc[0] < width - 1):
        ndata = getNewPos(pdata, wind, wind + 1)
        wres.append( [ndata, 1, "RIGHT", ndata[wind]])


    # CALCULATE UP MOVES
    if(wloc[1] > 0):
        ndata = getNewPos(pdata, wind, wind - width)
        wres.append( [ndata, 1, "UP", ndata[wind]])


    # CALCULATE DOWN MOVES
    if(wloc[1] < height - 1 ):
        ndata = getNewPos(pdata, wind, wind + width)
        wres.append( [ndata, 1, "DOWN", ndata[wind]])


    # CALCULATE WRAP MOVES
    if(wloc[0] == 0):
        ndata = getNewPos(pdata, wind, wind + (width - 1))
        wres.append( [ndata, 2, "WRAP LEFT", ndata[wind]])
    if(wloc[0] == width - 1):
        ndata = getNewPos(pdata, wind, wind - (width - 1))
        wres.append( [ndata, 2, "WRAP RIGHT", ndata[wind]])
    # if(wloc[1] == 0):
    #     ndata = getNewPos(pdata, wind, (width * (height -1) ) + wloc[0] )
    #     wres.append( [ndata, 2, "WRAP UP", ndata[wind]])
    # if(wloc[1] == height - 1 ):
    #     ndata = getNewPos(pdata, wind, wloc[0])
    #     wres.append( [ndata, 2, "WRAP DOWN", ndata[wind]])

    # CALCULATE CORNER MOVES
    if(height >= 2):
        if(wloc[0] == 0 and wloc[1] == 0):
            ndata = getNewPos(pdata, wind, (width * height) - 1)
            wres.append( [ndata, 3, "DIAGONAL UP-LEFT", ndata[wind]])
            ndata = getNewPos(pdata, wind, wind + width + 1)
            wres.append( [ndata, 3, "DIAGONAL DOWN-RIGHT", ndata[wind]])

        if(wloc[0] == width - 1  and wloc[1] == 0):
            ndata = getNewPos(pdata, wind, width * (height - 1) )
            wres.append( [ndata, 3, "DIAGONAL UP-RIGHT", ndata[wind]])
            ndata = getNewPos(pdata, wind, wind + width - 1)
            wres.append( [ndata, 3, "DIAGONAL DOWN-LEFT", ndata[wind]])

        if(wloc[0] == width - 1  and wloc[1] == height - 1):
            ndata = getNewPos(pdata, wind, (width * (height - 1)) - 2 )
            wres.append( [ndata, 3, "DIAGONAL UP-LEFT", ndata[wind]])
            ndata = getNewPos(pdata, wind, 0)
            wres.append( [ndata, 3, "DIAGONAL DOWN-RIGHT", ndata[wind]])

        if(wloc[0] == 0  and wloc[1] == height - 1):
            ndata = getNewPos(pdata, wind, (width * (height - 2)) + 1)
            wres.append( [ndata, 3, "DIAGONAL UP-RIGHT", ndata[wind]])
            ndata = getNewPos(pdata, wind, ( width - 1 ))
            wres.append( [ndata, 3, "DIAGONAL DOWN-LEFT", ndata[wind]])



    # print(wloc)
    # print("-------")
    return wres


def generateSolutions(pformat):
    height, width = pformat
    ret = []

    xcount = 0
    s1 = []
    for i in range(height):
        for j in range(width):
            xcount += 1
            if(xcount != width * height):
                s1.append(str(xcount))
            else:
                s1.append("0")
    ret.append(s1)

    xcount = 0
    s2 = []
    for i in range(height):
        for j in range(width):
            xcount += 1
            if(xcount != width * height):
                s2.append(str(i + 1 + height * j))
            else:
                s2.append("0")
    ret.append(s2)

    return ret



currentVisited = []
currentStack = []
currentSolution = []
cSolutions = []
solutionIndex = -1
cpFormat = []
start_time = 0;
solution_time = 0;


def getHeuristicVal(h, state):
    global cSolutions, cpFormat

    height, width = cpFormat
    xlen = height * width
    # print(xlen)
    ret = 0
    # h = 2

    if(h == -1):
        return 0
    if(h == 0):
        last = state[(height * width) - 1]
        if(last == "0"):
            return 0
        else:
            return 1
    if(h == 1):
        hmin = xlen
        for xsol in cSolutions:
            hval = 0
            for i in range(xlen):
                if(xsol[i] == state[i]):
                    hval += 1
            hmin = min(hmin, xlen - hval)
            # print(hval)
            # print(xlen - hval)
            # print(hmin)
            # print("====")
        
        return hmin
    if(h == 2):
        hmin = float('inf')
        for xsol in cSolutions:
            hval = 0
            for i in range(xlen):
                sti = state.index(xsol[i])
                sloc = [(i % width), int(i / width)]
                wloc = [(sti % width), int(sti / width)]

                xdist = abs(wloc[0] - sloc[0])
                ydist = abs(wloc[1] - sloc[1])
                xydist = xdist + ydist

                if(wloc[0] == 0 and sloc[0] == width - 1):
                    xydist = 2
                if(wloc[0] == width - 1 and sloc[0] == 0):
                    xydist = 2

                if(wloc[1] == 0 and sloc[1] == height - 1):
                    xydist = 2
                if(wloc[1] == height - 1 and sloc[1] == 0):
                    xydist = 2

                # TOP LEFT
                if(wloc[0] == 0 and wloc[1] == 0 and sloc[0] == 1 and sloc[1] == 1):
                    xydist = 3
                if(wloc[0] == 0 and wloc[1] == 0 and sloc[0] == width - 1 and sloc[1] == height - 1):
                    xydist = 3

                # BOT LEFT
                if(wloc[0] == 0 and wloc[1] == height - 1 and sloc[0] == 1 and sloc[1] == height - 2):
                    xydist = 3
                if(wloc[0] == 0 and wloc[1] == height - 1 and sloc[0] == width - 1 and sloc[1] == 0):
                    xydist = 3


                # TOP RIGHT
                if(wloc[0] == width - 1 and wloc[1] == 0 and sloc[0] == width - 2 and sloc[1] == 1):
                    xydist = 3
                if(wloc[0] == width - 1 and wloc[1] == 0 and sloc[0] == 0 and sloc[1] == height - 1):
                    xydist = 3

                # BOT RIGHT
                if(wloc[0] == width - 1 and wloc[1] == height - 1 and sloc[0] == width - 2 and sloc[1] == height - 2):
                    xydist = 3
                if(wloc[0] == width - 1 and wloc[1] == height - 1 and sloc[0] == 0 and sloc[1] == 0):
                    xydist = 3

                hval += xydist

                
            # print(hval)
            hmin = min(hmin, hval)
            # print(hmin)
            # print("====")
        return hmin
    return 0

def reorderKey(elem):
    return elem[1]

def solutionFinder(heuristic, algo):
    global currentStack, currentSolution, currentVisited, cSolutions, cpFormat, solutionIndex, start_time, solution_time

    newStack = []
    solutionFound = False
    solutionCost = float('inf')
    loopcount = 0

    if(len(currentStack) > 0):
        # for i in currentStack:
        while len(currentStack) > 0:
            loopcount += 1
            # print(len(currentStack))
            if(not solutionFound):
                currentStack.sort(key=reorderKey)
                # print(currentStack[0][1])
                # print(currentStack[len(currentStack) - 1][1])
                # if(currentStack[len(currentStack) - 1][1] <= currentStack[0][1]):
            xstate = currentStack.pop(0)

            # if(loopcount > 20):
            #     break
                # for e in currentStack:
                #     print(e[1])
            # print(xstate)
            # print(currentVisited)
            currentState = xstate[0]
            currentCost = xstate[1]
            currentPath = xstate[2]
            currentDir = xstate[3]

            currentTiles = xstate[4][0]
            currentStepCost = xstate[4][1]
            currentNodeCost = xstate[4][2]
            currentHCost = xstate[4][3]

            if(loopcount % 1000 == 0):
                current_time = time.time() - start_time
                if(current_time > 60):
                    break
            if(loopcount % 10000 == 0):
                print("Current Loop: " + str(loopcount), end = "")
                print(" | Time: %s secs" % (current_time))
                print("Stack Size: " + str(len(currentStack)), end = "")
                print(" | Cost Range: [" + str(currentCost) + " - " + str(currentStack[len(currentStack) - 1][1]) + "]")


            # currentPath.append(currentState.copy())
            # currentDir.append(currentState.copy())


            if(solutionFound and currentCost >= solutionCost):
                # print("FOUND SOLUTION WITH COST SKIPPING")
                continue

            stateVisited = False
            for visited in currentVisited:
                if(currentState == visited[0]):
                    stateVisited = True
                    break

            if(stateVisited):
                # print("STATE VISITED")
                # print(currentState)
                continue
            else:
                sindex = -1
                for sol in cSolutions:
                    sindex += 1
                    if(sol == currentState):
                        solution_time = time.time() - start_time
                        print("=============")
                        print("SOLUTION FOUND")
                        print("Current Loop: " + str(loopcount))
                        # print("Stack Size: " + str(len(currentStack)))
                        print("Solution Time: %s secs" % (solution_time))
                        print("Solution Cost: " + str(currentCost))
                        print("Solution Path: ", end="")
                        print(currentDir)

                        solState = xstate.copy()
                        solState[2].append(currentState)
                        solState[3].append("SOLUTION")
                        # print(currentPath)
                        solutionFound = True
                        solutionCost = currentCost
                        solutionIndex = sindex
                        currentSolution = solState
                        printPuzzle(cSolutions[solutionIndex], cpFormat, False, "")
                        print("=============")
                        break

                currentVisited.append( xstate )
                
                pmoves = getPosibleMoves(xstate[0], cpFormat)
                for newState in pmoves:
                    stepState = newState[0]
                    stepCost = newState[1]
                    stepDirection = newState[2]
                    stepTile = newState[3]

                    nodeCost = currentCost

                    if(algo == "UCS"):
                        hval = 0
                    else:
                        hval = getHeuristicVal(heuristic, stepState)

                    if(algo == "GBFS"):
                        nodeCost = 0
                    
                    if(solutionFound and nodeCost + stepCost + hval >= solutionCost):
                        continue
                        # print(currentCost + stepCost)
                        # if(solutionFound):
                        #     print(currentCost + stepCost)
        
                    
                    moveVisited = False
                    for visited in currentVisited:
                        if(stepState == visited[0]):
                            moveVisited = True
                            break
                    if(moveVisited):
                        # print("MOVE VISITED")
                        continue

                    movePath = currentPath.copy()
                    movePath.append(currentState.copy())

                    moveDir = currentDir.copy()
                    moveDir.append(stepDirection)



                    moveTile = currentTiles.copy()
                    moveTile.append(stepTile)

                    moveStepCost = currentStepCost.copy()
                    moveStepCost.append(stepCost)

                    moveNodeCost = currentNodeCost.copy()
                    moveNodeCost.append(nodeCost)

                    moveHCost = currentHCost.copy()
                    moveHCost.append(hval)


                    currentStack.append( [stepState, nodeCost + stepCost + hval, movePath, moveDir, [moveTile, moveStepCost, moveNodeCost, moveHCost] ] )

    # print("/////////////////////")
    # print("Algorithm Finished")
    # print("Final Loops: " + str(loopcount))
    # print("/////////////////////")

    if(solutionIndex > -1):
        # print("Solution Found")
        # print("Solution Time: %s secs" % (solution_time))
        # print("Solution Cost: " + str(currentSolution[1]))
        # print("Solution Path: ", end="")
        # print(currentSolution[3])
        
        solStates = currentSolution[2]
        solTiles = currentSolution[4][0]
        solStepCosts = currentSolution[4][1]
        solNodeCosts = currentSolution[4][2]
        solHCosts = currentSolution[4][3]

        # BUILD SOLUTION STRING
        solutionstring = ""
        for i in range(len(currentSolution[3])):
            if(i > 0):
                solutionstring += "\n"
            solutionstring += solTiles[i]
            solutionstring += " " + str(solStepCosts[i])
            for s in solStates[i]:
                solutionstring += " " + str(s)
        # print(solutionstring)

        # BUILD SEARCH STRING
        searchstring = ""
        for i in range(len(currentVisited)):
            if(i > 0):
                searchstring += "\n"
            tailI = len(currentVisited[i][4][0]) - 1
            searchfval = currentVisited[i][1]
            # searchTile = currentVisited[i][4][0][tailI]
            searchStepCosts = currentVisited[i][4][1][tailI]
            searchNodeCosts = currentVisited[i][4][2][tailI]
            searchHCosts = currentVisited[i][4][3][tailI]

            searchstring += str(searchfval)
            searchstring += " " + str( int(searchNodeCosts) )
            searchstring += " " + str( int(searchStepCosts) + int(searchHCosts)  )
            for s in currentVisited[i][0]:
                searchstring += " " + str(s)
            
            # print(searchfval)
            # print(int(searchStepCosts))
            # print(int(searchHCosts))
            # print(int(searchNodeCosts))
            # print("=====")
            # print(currentVisited[i])
        # print(searchstring)
        
        # for i in range(len(currentSolution[2])):
        #     printPuzzle(currentSolution[2][i], cpFormat, False, "")
        #     print(currentSolution[3][i])
        
        printPuzzle(cSolutions[solutionIndex], cpFormat, False, "")
    else:
        print("NO SOLUTION FOUND")
        solutionstring = "no solution"
        searchstring = "no solution"

    return solutionstring, searchstring





def generatePuzzles(pformat, n):
    height, width = pformat
    ret = []
    retstr = ""
    for j in range(n):
        pz = []
        if(j > 0):
            retstr += "\n"
        for i in range(height * width):
            pz.append(str(i))
        random.shuffle(pz)
        for i in range(height * width):
            if(i == 0):
                retstr += str(pz[i])
            else:
                retstr += " " + str(pz[i])
        ret.append(pz)


    # print(retstr)


    f = open("randomPuzzles.txt", "w")
    f.write(retstr)
    f.close()

    return ret



def restartGlobals():
    global currentVisited, currentStack, currentSolution, solutionIndex, solution_time

    currentVisited = []
    currentStack = []
    currentSolution = []
    solutionIndex = -1
    solution_time = 0

    return

def saveSolution(solutionstring, searchstring, index, algostr):
    fstring = str(index) + "_" + algostr
    f = open(fstring + "_solution.txt", "w")
    f.write(solutionstring)
    f.close()
    f = open(fstring + "_search.txt", "w")
    f.write(searchstring)
    f.close()
    print(fstring + " => SAVED")

def analizeSolutions(lstr, sarray):
    astr = ""

    solsum, searchsum, nosolsum, timesum, nosolsum = 0, 0, 0, 0, 0
    for e in sarray:
        solsum += e[0]
        searchsum += e[1]
        timesum += e[2]
        nosolsum += int(e[4])
    solavg = solsum / len(sarray)
    searchavg = searchsum / len(sarray)
    nosolavg = nosolsum / len(sarray)
    timeavg = timesum / len(sarray)

    astr += "Analysis of Algorithm: " + lstr + "\n"
    astr += "=====\n"
    astr += "Average Solution Length: " + str(solavg) + "\n"
    astr += "Total Solution Length: " + str(solsum) + "\n"

    astr += "Average Search Length: " + str(searchavg) + "\n"
    astr += "Total Search Length: " + str(searchsum) + "\n"

    astr += "Average No Solution: " + str(nosolavg) + "\n"
    astr += "Total No Solution: " + str(nosolsum) + "\n"

    astr += "Average Execution Time: " + str(timeavg) + "\n"
    astr += "Total Execution Time: " + str(timesum) + "\n"


    f = open(lstr + "_analysis.txt", "w")
    f.write(astr)
    f.close()
    print(astr)

def puzzleSolver(puzzle, algo, heuristic, pformat, index):
    global currentStack, cSolutions, cpFormat, start_time

    cpFormat = pformat
    cSolutions = generateSolutions(pformat)
    # for sol in cSolutions:
    #     printPuzzle(sol, pformat, False, "Solution Array")

    restartGlobals()
    start_time = time.time()
    



    # printPuzzle(puzzle, pformat, False, algo)
    
    currentStack = [ [puzzle, 0, [], [], [ ['0'], [0], [0], [0] ]] ]
    # print(getHeuristicVal(heuristic, puzzle))
    algostr = ""
    if(algo == "UCS"):
        algostr = "ucs"
        print("Searching Algorithm: Uniform Cost (UCS)")
    if(algo == "GBFS"):
        algostr = "gbfs-h" + str(heuristic)
        print("Searching Algorithm: Greedy Best First (GBFS)")
        print("Solving for Heuristic: " + str(heuristic) )
    if(algo == "A*"):
        algostr = "astar-h" + str(heuristic)
        print("Searching Algorithm: Algorithm A* (A*)")
        print("Solving for Heuristic: " + str(heuristic) )
    solutionstring, searchstring = solutionFinder(heuristic, algo)
    saveSolution(solutionstring, searchstring, index, algostr)


    ftime = time.time() - start_time
    print("--- %s seconds ---" % ( ftime ))

    solStepCosts = 0
    solutionLength = 0
    if(len(currentSolution) > 0):
        solStepCosts = currentSolution[4][1]
        solutionLength = len(currentSolution[3])
    searchLength = len(currentVisited)
    noSolution = solutionstring == "no solution"

    return solutionLength, searchLength, ftime, solStepCosts, noSolution