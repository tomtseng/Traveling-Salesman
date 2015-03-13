##Traveling Salesman Problem Visualization
Lets user place locations on a canvas and generates a short Hamiltonian cycle
traversing those locations.  User may choose between finding an exact solution
or an approximate solution. The number of locations that the user many place if
finding the exact solution is severely limited because the traveling salesman
problem is NP-hard, and the calculation is sluggish beyond about 15 locations.

Click on the empty space to add or remove locations.

###Keyboard shortcuts:
Press the space bar to calculate.

Press 'r' to reset.

Press 'p' to add a random location.

* * *
The code for calculating the Hamiltonian cycle is sketchy. I may clean it up in
the future.

It would be interesting to implement a simulated annealing approximation
algorithm in the future. The current approximation algorithm just generates a
minimum spanning tree and travels along that.
