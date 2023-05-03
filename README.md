# Pathfinding_Visualiser
Pathfinding Visualiser implementation in python and pygame.

## Running the program
- In order to run the program with the arguments, you need to open the console on windows and type python or python3 if you have both versions followed     by the name of the file you will be running followed by the filename and then the name of the search.
  
**Example on how you can run the program with the 6 searches.**
  * python3 main.py map.txt BFS
  * python3 main.py map.txt DFS
  * python3 main.py map.txt GBFS
  * python3 main.py map.txt GBFS
  * python3 main.py map.txt BAstar
  * python3 main.py map.txt IDS
 
 
 ## Using the GPU
* After you run the application, the GPU will open and the map will be drawn based on the file provided. You can run the searches using Keyboard keys. B for Breadth First Search (BFS), A for Astar(A*), G for Greedy Best first search (GBFS), D for Depth First Search(DFS), I for IDAstar(IDA*) and F for Bidirectional A* search(BBFS).
* Left click by the mouse will add walls to the map, right click will delete the walls and if you want to add or delete goals you stop by the mouse in wanted square and press W.
* C will clear the GUI from the previous search and R will reset the map to the initial map.
* After each search the actual time taken to perform the search, the number of nodes visited and the path cost will be print to the GUI under the map.
* To install pygame on windows 10, open the command prompt and give the command “pip install pygame”



**Note**
You can’t run other search in the GUI while there is other search that is taking place.

## Text file format
* First line contains a pair of numbers [N,M] – the number of rows and the number of columns of the
grid, enclosed in square brackets.
* Second line contains a pair of numbers (x1,y1)– the coordinates of the current location of the agent,
the initial state.
* Third line contains a sequence of pairs of numbers separated by |; these are the coordinates of the
goal states: (x G1,y G1) | (x G2,y G2) | ... | (x Gn,y Gn), where n ≥ 1
* The subsequent lines represent the locations of the walls: The tuple (x,y,w,h) indicates that the
leftmost top corner of the wall occupies cell (x,y) with a width of w cells and a height of h cells.
* It is assumed that the text file will containg valid configurations.


 
 

