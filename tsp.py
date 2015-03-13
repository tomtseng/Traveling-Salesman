from Tkinter import *
import ttk
import math
import random
import itertools
import Queue

locations = []
isDone = False;

radius = 4
canvSize = 400
canvBorder = 5

# Pre: t1, t2 2-tuple of coordinates
# Post: returns euclidean distance
def dist(t1, t2):
    return math.hypot((t1[0]-t2[0]),(t1[1]-t2[1]))

def restoreDone():
    global isDone
    if isDone == True:
        isDone = False
        calcBtn.config(text="Calculate", state=NORMAL)
        canvas.delete("line");

def keyPress(event):
    global isDone
    if (event.char == " ") and (isDone == False): makeTour()
    elif (event.char == "r"): reset()
    elif (event.char == "p"): addRand()

def reset():
    global locations, isDone
    canvas.delete(ALL)
    locations = []
    restoreDone()

def click(event):
    global locations, radius
    restoreDone()
    xy = (event.x, event.y)
    for (l,I) in locations:
        if (dist(xy, l) <= radius):
            removePoint(l,I)
            return
    addPoint(xy)

# Pre: (l,I) in locations
# Post: removes l from locations and removes appropriate point on canvas
def removePoint(l,I):
    global locations
    locations.remove((l,I))
    canvas.delete(I)

# Pre: coord is a 2-tuple
# Post: adds coord to locations and draws appropriate point
def addPoint(coord):
    global locations, radius
    maxLocs = 15 if (isApprox.get() == 0) else 500
    if (len(locations) < maxLocs):
        x0 = coord[0] - radius
        y0 = coord[1] - radius
        x1 = coord[0] + radius
        y1 = coord[1] + radius
        ID = canvas.create_oval(x0, y0, x1, y1, fill='red')
        locations.append((coord,ID))


def addRand():
    global canvSize, canvBorder
    restoreDone()
    low = canvBorder
    high = canvSize-1-canvBorder
    coord = (random.randint(low, high), random.randint(low, high))
    addPoint(coord)

# Post: Outputs a permutation of locations that represents a traveling
#       salesman tour.
# Uses dynamic programming approach. O(n^2*2^n) time complexity.
# Implementation is heavily based off of:
# http://www.digitalmihailo.com/
# traveling-salesman-problem-dynamic-algorithm-implementation-in-python/
def exactTour():
    global locations
    leng = len(locations)
    if (leng <= 2):
        return locations

    # distances between any two points
    distances = [[dist(xy1,xy2) for (xy2,I) in locations] 
                for (xy1,I) in locations]
    # (distance, pathTaken) from 1st point to every point
    dp = {(frozenset([0,i+1]), i+1): (dist, [0,i+1]) 
          for (i,dist) in enumerate(distances[0][1:])}
    for k in xrange(2, leng): # k is size of subproblem (size of subset)
        dpTemp = {}
        # for each subset of size k containing location 0...
        for S in [frozenset(A) | {0} for A in 
                  itertools.combinations(xrange(1, leng), k)]:
            for j in S - {0}:
                dpTemp[(S,j)] = min([(dp[(S-{j},p)][0] + distances[j][p], 
                                     dp[(S-{j},p)][1] + [j]) 
                                     for p in S - {0,j}])
        dp = dpTemp
    path = min([(dp[key][0] + distances[0][key[1]], dp[key][1])
                  for key in dp.keys()])
    return [locations[i] for i in path[1]]

# Post: Outputs a permutation of locations that represents a traveling
#       salesman tour approximation.
# Finds MST using Prim's algorithm and creates tour using DFS. 
# O(n^2) time complexity.
def approxTour():
    global locations
    leng = len(locations)
    if (leng <= 2):
        return locations

    distances = [[dist(xy1,xy2) for (xy2,I) in locations] 
                 for (xy1,I) in locations]

    mst = [set() for _ in range(leng)]
    unvisited = range(1,leng)
    pq = Queue.PriorityQueue()
    # place all edges out of point 0 in priority queue
    for i in xrange(1, leng): pq.put((distances[0][i], (0,i)))
    while unvisited:
        edge = pq.get()[1]
        v1, v2 = edge[0], edge[1]
        if v2 in unvisited:
            mst[v1] = mst[v1] | {v2}
            mst[v2] = mst[v2] | {v1}
            unvisited.remove(v2)
            for u in xrange(1, leng):
                if u in unvisited: pq.put(((distances[v2][u]), (v2,u)))

    path = []
    stack = [0]
    while stack:
        vertex = stack.pop()
        if vertex not in path:
            path.append(vertex)
            stack.extend([j for j in xrange(leng) if j not in path
                          and j in mst[vertex]])

    return [locations[i] for i in path]

# Pre: Takes some permutation of locations
# Post: Draws lines between permutation in order
def drawTour(tour):
    for i in xrange(-1, len(tour)-1):
       canvas.create_line(tour[i][0][0], tour[i][0][1], 
                          tour[i+1][0][0], tour[i+1][0][1], width=2, tag="line")

def makeTour():
    global isDone
    calcBtn.config(state=DISABLED)
    tour = exactTour() if (isApprox.get() == 0) else approxTour()
    drawTour(tour);
    isDone = True;
    calcBtn.config(text="Done!")

root = Tk()
root.resizable(0,0)

canvas = Canvas(root, width=canvSize, height=canvSize, bd=canvBorder)
calcBtn = ttk.Button(text="Calculate", command=makeTour)
randomBtn = ttk.Button(text="Add pseudorandomly", command=addRand, 
                       takefocus=False)
resetBtn = ttk.Button(text="Reset", command=reset, takefocus=False)
isApprox = IntVar()
approxChk = ttk.Checkbutton(text="Approximate", variable=isApprox, 
                            command=reset, takefocus=False)

canvas.grid(column=0, row=0, columnspan=4)
calcBtn.grid(column=0, row=1)
randomBtn.grid(column=1, row=1)
resetBtn.grid(column=2, row=1)
approxChk.grid(column=3, row=1)

canvas.bind("<Button-1>", click)
root.bind("<Key>", keyPress)

root.mainloop()
