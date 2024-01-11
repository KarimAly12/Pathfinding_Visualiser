from collections import deque
import pygame
import threading
import time
import _thread
from graph import*
from world import*
from searches import*
import threading
import sys
import copy

BFS = "BFS"
DFS = "DFS"
GBFS = "GBFS"
ASTAR = "AS"
BBFS = "BBFS"
IDS = "IDS"
BASTAR = "BAstar"

def dfs(_searches:Searches, world:World):
    dfs_node = _searches.DFS(world.agent_start_pos)
    node = dfs_node
    if dfs_node == None: return None
    print("Filename = " + sys.argv[1])
    print("Depth  First Search")
    print("Number of nodes visited = " + str(len(_searches.node_visited_list)))
    dfs_search_path_dir = []
    while dfs_node != None:
        #world.path.append(dfs_node.state)
        dfs_search_path_dir.append(dfs_node.action)
        dfs_node = dfs_node.parent

    for i in range(len(dfs_search_path_dir)-1, -1, -1):
        print(dfs_search_path_dir[i])
    print("---------------------")    
    return node


def bfs(_searches:Searches, world:World):
    bfs_node = _searches.BFS(world.agent_start_pos)
    node = bfs_node
    if bfs_node == None: return None
    print("Filename = " + sys.argv[1])
    print("Breadth  First Search")
    print("Number of nodes visited = " + str(len(_searches.node_visited_list)))
    bfs_search_path_dir = []
    while bfs_node != None:
        #world.path.append(bfs_node.state)
        bfs_search_path_dir.append(bfs_node.action)
        bfs_node = bfs_node.parent

    for i in range(len(bfs_search_path_dir)-1, -1, -1):
        print(bfs_search_path_dir[i])
    print("---------------------")    
    return node


def astar(_searches:Searches, world:World):
    astar_node:Node = _searches.aStar(world.agent_start_pos)
    node = astar_node
    if astar_node == None: return None
    print("Filename = " + sys.argv[1])
    print("Astar Search")
    print("Number of nodes visited = " + str(len(_searches.node_visited_list)))
    astar_search_path_dir = []
    while astar_node != None:
        #world.path.append(astar_node.state)
        astar_search_path_dir.append(astar_node.action)
        astar_node = astar_node.parent

    for i in range(len(astar_search_path_dir)-1, -1, -1):
        print(astar_search_path_dir[i])
    print("---------------------")    
    return node


def gbfs(_searches:Searches, world:World):
    gbfs_node = _searches.gbfs(world.agent_start_pos)
    node = gbfs_node
    if gbfs_node == None: return None
    print("Filename = " + sys.argv[1])
    print("Greedy Best First Search")
    print("Number of nodes visited = " + str(len(_searches.node_visited_list)))
    gbfs_search_path_dir = []
    while gbfs_node != None:
        #world.path.append(gbfs_node.state)
        gbfs_search_path_dir.append(gbfs_node.action)
        gbfs_node = gbfs_node.parent

    for i in range(len(gbfs_search_path_dir)-1, -1, -1):
        print(gbfs_search_path_dir[i])
    print("---------------------")    
    return node

# def bbfs(_searches:Searches, world:World):
#     print("Filename = " + sys.argv[1])
#     print("Bidirectional Breadth First Search")
#     bibs_node = _searches.BBFS(world.agent_start_pos)
#     node = bibs_node
#     print("Number of nodes visited = " + str((len(_searches.node_visited_list) + len(_searches.node_visited_list_b))))
#     bbfs_search_path_dir = []
#     while bibs_node != None:
#         #world.path.append(bibs_node.state)
#         bbfs_search_path_dir.append(bibs_node.action)
#         bibs_node = bibs_node.parent

#     for i in range(len(world.path)-1, -1, -1):
#         print(bbfs_search_path_dir[i])
#     print("---------------------")    
#     return node


# def idastar(_searches:Searches, world:World):
#     print("Filename = " + sys.argv[1])
#     print("IDastar Breadth First Search")
#     idastar_node = _searches.IDAstar(world.agent_start_pos)
#     node = idastar_node
#     print("Number of nodes visited = " + str((len(_searches.node_visited_list))))
#     idastar_search_path_dir = []
#     while idastar_node != None:
#         #world.path.append(idastar_node.state)
#         idastar_search_path_dir.append(idastar_node.action)
#         idastar_node = idastar_node.parent

#     for i in range(len(idastar_search_path_dir)-1, -1, -1):
#         print(idastar_search_path_dir[i])
#     print("---------------------") 
#     return node   




#Becuase of the joined nodes in 



# def bastar(_searches:Searches, world:World):
#     search_node = _searches.BAstar(world.agent_start_pos)
#     node = search_node
#     if search_node == None: return None
#     print("Filename = " + sys.argv[1])
#     print("Bidirectional A* Search")
#     print("Number of nodes visited = " + str((len(_searches.node_visited_list) + len(_searches.node_visited_list_b))))
#     search_path_dir = modify_BAstar_actions(search_node)
#     #print(search_node.state)
#     #print(search_node.parent.action)
#     #node_state = search_node.state
#     for i in  range(len(search_path_dir)):
#         print(search_path_dir[i])

#     # while search_node != None:
#     #     #world.path.append(bibs_node.state)
#     #     search_path_dir.append(search_node.action)
#     #     search_node = search_node.parent
#     # if world.graph.graph[node_state[1]][node_state[0]] in world.goals:
#     #     for i in range(len(search_path_dir)-1, -1, -1):
#     #         print(search_path_dir[i])
#     # else:
#     #      for i in range(len(search_path_dir)-1):
#     #         print(search_path_dir[i])
#     print("---------------------")    
#     return node


def ids(_searches:Searches, world:World):
    ids_node = _searches.IDS(world.agent_start_pos)
    node = ids_node
    if ids_node == None: return None
    print("Filename = " + sys.argv[1])
    print("Iterative deepening Search")
    print("Number of nodes visited = " + str((len(_searches.node_visited_list))))
    search_path_dir = []
    while ids_node != None:
        #world.path.append(idastar_node.state)
        search_path_dir.append(ids_node.action)
        ids_node = ids_node.parent

    for i in range(len(search_path_dir)-1, -1, -1):
        print(search_path_dir[i])
    print("---------------------") 
    return node   




def execute_search(search_name, searches:Searches, world:World):
    if search_name == BFS:
       return bfs(searches, world)
    elif search_name == GBFS:
       return gbfs(searches, world)
    elif search_name == ASTAR:
        return astar(searches, world)
    elif search_name == DFS:
        return dfs(searches, world)
    #elif search_name == BBFS:
        #return bbfs(searches, world)
    elif search_name == IDS:
        return ids(searches, world)
    # elif search_name == BASTAR:
    #     return bastar(searches, world)


def check_key_event_for_search(searches, world:World):
    keys = pygame.key.get_pressed()
    for key, value in searches.items():
        # if a keyboard key is pressed clear the world to be ready for new search and return the key
        if keys[key]:
            world.clear_world()
            return key, value
        #else return -1
    return -1, ""




def main():
    world:World =None
    
    try:
        world = World(sys.argv[1])
    except FileNotFoundError:
        print(sys.argv[1] + " file not found")
        return

    node:Node = None
    visulaiser_counter:int =0
    robot_nav_problem = Robot_Nav_Problem()
    searches:Searches = Searches(world, robot_nav_problem)

    node = execute_search(sys.argv[2], searches, world)
    if node == None:
        print("No Solution Found")





    #dfs_path()
    #bfs_path()
    #astar_path()
    #gbfs()

    #to start a search press its key
    searches_keys =  {
        pygame.K_b :BFS,
        pygame.K_a:ASTAR,
        pygame.K_g:GBFS,
        pygame.K_d:DFS,
        pygame.K_i:IDS,
        pygame.K_f:BBFS,
        pygame.K_y:BASTAR
    
    }  

    search_key:int = -1 # no key is pressed

    world.reset_world()
    world.clear_world()
    searches.reset_searches()

    search_name = ""
    
    while world.running:

        world.event_handler()
        world.render()

        # as long as no key is pressed check if the user pressed any key
        if search_key == -1:
            search_key, search_name = check_key_event_for_search(searches=searches_keys, world=world)


        if search_key != -1 and search_name != "":
            #perfrom search if the node is None and return the goal node
            if node == None:
                searches.reset_searches()
                node = execute_search(search_name, searches, world)
                if node == None:
                    search_key = -1
                    search_name = ""
                    print("No soluction found")
           
            #every NUM increments set one of the visited nodes of the search to isVisited = true
            #it will be drawen by the render function in the world class
            if(visulaiser_counter >= 10):
                visulaiser_counter=0
               
                if len(searches.node_visited_list) > 0 or len(searches.node_visited_list_b) > 0:
                    world.set_cell_visited(searches.node_visited_list, searches.node_visited_list_b)                              
        visulaiser_counter+=1
        
        # if there is no nodes in the list of the visited nodes and the node 
        # is not null add the path to the list to be drawn by the render function in the world class
        if(len(searches.node_visited_list) == 0 and len(searches.node_visited_list_b) == 0):
            while (node != None):
                world.path.append(node.state)
                node = node.parent
        
            search_key = -1
            #execute_search(search_name, searches, world)
            search_name = ""
            
           

        pygame.display.flip()
        
    pygame.quit()


        

    
if __name__ == "__main__":
    
    main()
    
    # print(world.graph.bfs(start_pos = world.agent_start_pos).state)
    # print(world.graph.dfs(start_pos=world.agent_start_pos).state)

    


