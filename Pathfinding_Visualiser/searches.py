from graph import Graph 
from graph import Node
from typing import TypeVar, Generic
from queue import PriorityQueue
from cell import Cell
from collections import deque
import math
import time
import pygame
from world import World
from search_helper_functions import*
from heuristics import*
import copy
from abc import ABC, abstractmethod



class Problem(ABC):
    @abstractmethod
    def expand(self, node:Node):
        pass

#Robot_Nav_problem is a child of the parent class Problem
class Robot_Nav_Problem(Problem):
    def expand(self, node: Node, graph):
        state = node.state
        nodes:list[Node] = []
        #return all the actions that can be applied on the current node state
        actions = self.action_applied_onStates(state, graph)
        for key, value in actions.items():
            #apply action on the current state and return the new state
            s = actions[key](state)
            cost = node.path_cost + 1
            nodes.append(Node(state=s, parent=node, action = key, path_cost=cost))
        return nodes
    #return a dictionary of actions that can be applied on a node state. 
    #The function name is the key and the value is a lamada function. 
    #The order of actions on state is UP,LEFT,DOWN,RIGHT
    def action_applied_onStates(self,state, graph):
        state_actions = {}
        if(state[1] > 0 and not graph[state[1] -1][state[0]].is_wall):
            state_actions["UP"] = lambda pos: (pos[0], pos[1] -1)
        if(state[0] > 0 and not graph[state[1]][state[0]-1].is_wall):
            state_actions["LEFT"] = lambda pos: (pos[0] - 1, pos[1])
        if(state[1] < len(graph) - 1 and not graph[state[1]+1][state[0]].is_wall):
            state_actions["DOWN"] =  lambda pos: (pos[0], pos[1] + 1)
        if(state[0] < len(graph[0]) -1 and not graph[state[1]][state[0] + 1].is_wall):
            state_actions["RIGHT"] = lambda pos: (pos[0] +1, pos[1])
        return state_actions
    
    
        




class Searches:
    def __init__(self, world:World, problem:Problem) -> None:
        #self.graph = graph
        self.world:World = world
        #self.reached_nodes = {}
        #self.frontier = deque()
        #self.reached = []
        #self.node:Node = None
        #self.reached_nodes = {}
        #self.pq = PriorityQueue() 
        #self.goal:Cell = None
        #self.distacne_to_goal = 0
        #self.depth_limit = 0
        #self.is_expand = False
        self.node_visited_list = []
        #self.min_fscore = []
        self.BIBF_test = False
        self.node_visited_list_b = []
        self.problem = problem
       
    """
    Depth first search uses LIFO Stack.
    It doesn't gurantee the shortest path and it is uninformed search.
    """
    def DFS(self, start_pos):
        #the time when the search start.
        start_time = time.time()
        node:Node = Node(state=start_pos)
        if self.world.graph.graph[node.state[1]][node.state[0]].is_goal:
            self._add_search_details("Depth first search", start_time, node)
            return node
        #LIFO frontier
        stack = deque()
        reached = []
        stack.append(node)
        while len(stack) > 0:
            node = stack.pop()
            reached.append(node.state)
            if(node.state != start_pos):
                #append the node the visited list.The list will be used to visualise the search algorithm.
                self.node_visited_list.append(node)
            nodes:list[Node] = self.problem.expand(node, self.world.graph.graph)
            #iterate backwardly as the actions in the expanded list are in the order UP-LEFT-DOWN-RIGHT. UP must be added the stack last as stack is LIFO.
            for i in range(len(nodes)-1,-1, -1):
                s = nodes[i].state
                if self.world.graph.graph[s[1]][s[0]].is_goal:
                    self.node_visited_list.append(nodes[i])
                    self._add_search_details("Depth first search", start_time, nodes[i])
                    #return the node if it is the goal.
                    return nodes[i]
                #check that we have not reached that state before.
                if not s in reached:
                    stack.append(nodes[i])
                    #reached.append(s)
        #Return None if was unable to find solution.
        return None


    """
    Breadth first search uses FIFO Que.
    It gurantee the shortest path and it is uninformed search.
    """ 
    def BFS(self, start_pos):
        #the time when the search start.
        start_time = time.time()
        #keep track of the reached nodes
        reached = []
        #initial node with the initial State
        node = Node(state=start_pos, parent=None) 
        if self.world.graph.graph[node.state[1]][node.state[0]].is_goal:
            self._add_search_details("Breadth first search", start_time=start_time, node=node)
            return node
        #FIFO frontier
        q = deque()
        q.append(node)
        reached.append(node.state)
        while len(q)>0:   
            node = q.popleft()

            if(node.state != start_pos):
                #this list will be used to visualise the search
                self.node_visited_list.append(node)
            nodes:list[Node] = self.problem.expand(node, self.world.graph.graph)
            for child in nodes:
                s = child.state
                if self.world.graph.graph[s[1]][s[0]].is_goal:
                    self.node_visited_list.append(child)
                    self._add_search_details("Breadth first search", start_time=start_time, node =child)
                    return child
                # add node to q if its state is not reached
                if not s in reached:
                    reached.append(s)
                    q.append(child)
        return None
    
    # def dijkstra(self, start_pos):
    #     start_time = time.time()
    #     node = Node(state=start_pos)
    #     pq:PriorityQueue = PriorityQueue()
    #     pq.put((node.path_cost, node))
    #     reached_nodes= {}
    #     reached_nodes[node.state] = node
    #     while(pq.qsize() > 0):
    #         node = pq.get()[1]
    #         if(node.state != start_pos):
    #             self.node_visited_list.append(node)
    #         if self.world.graph.graph[node.state[1]][node.state[0]].is_goal:
    #             self._add_search_details("Dijkstra best first search", start_time, node)
    #             return node
    #         nodes:list[Node] = self.__expandNodes(node)
    #         for i in range(len(nodes)):
    #             if not nodes[i].state in reached_nodes or reached_nodes[nodes[i].state].path_cost > nodes[i].path_cost:
    #                 reached_nodes[nodes[i].state] = nodes[i]
    #                 pq.put((nodes[i].path_cost, nodes[i]))
    #     return None

    """
    Greadth best first search uses Priority Queue.
    It doesn't gurantee the shortest path and it is informed search.
    """ 
    def gbfs(self, start_pos):
        #the time when the search start.
        start_time = time.time()
        #initial node with the initial state
        node = Node(state=start_pos)
        #return the closes goal to the initial agent position
        goal = self.closest_goal_to_cell(self.world.graph.graph[node.state[1]][node.state[0]])

        if goal != None:
            #get the distance from the current state to the goal(heuristic function)
            distacne_to_goal = manhatan(node, Node(state=goal.pos))
            #priotiy queue priorise the nodes based on evaluation function (distance_to_goal)
            pq:PriorityQueue = PriorityQueue()
            pq.put((distacne_to_goal, node))
            reached_nodes= {
                node.state: node
            }
            while(pq.qsize() > 0):
                node = pq.get()[1]
                if(node.state != start_pos):
                    #this list will be used to visualise the search
                    self.node_visited_list.append(node)
                    #retrun the goal node once it is found and set the search details
                if self.world.graph.graph[node.state[1]][node.state[0]].is_goal:
                    self._add_search_details("Greedy best first search", start_time, node)
                    return node
                nodes:list[Node] = self.problem.expand(node, self.world.graph.graph)
                for i in range(len(nodes)):
                    #add the node to pq if its state is not reached or if the state reached has higher cost
                    if not nodes[i].state in reached_nodes or reached_nodes[nodes[i].state].path_cost > nodes[i].path_cost:
                        #get the closeset goal to the state
                        goal = self.closest_goal_to_cell(self.world.graph.graph[nodes[i].state[1]][nodes[i].state[0]])
                        #get the distance from the current state to the goal(evaluation function)
                        distacne_to_goal = manhatan(nodes[i], Node(state=goal.pos))
                        reached_nodes[nodes[i].state] = nodes[i]
                        pq.put((distacne_to_goal, nodes[i]))
        return None
    

  

    """
    Astar search uses Priority Queue.
    It gurantee the shortest path and it is informed search.
    """ 
    def aStar(self, start_pos):
        # The time when the search starts.
        start_time = time.time()
        # Initial node with initial state
        node = Node(state=start_pos)
        # The goal closest to the current state
        goal = self.closest_goal_to_cell(self.world.graph.graph[node.state[1]][node.state[0]])
        if goal != None:
            # Get the distance from the current state to the goal (heuristic function)
            distance_to_goal = manhatan(node, Node(state=goal.pos))
            print(distance_to_goal)
            # Priority queue prioritizes the nodes based on the heuristic function + node path_cost
            pq: PriorityQueue = PriorityQueue()
            pq.put((distance_to_goal + node.path_cost, node))
            # To keep track of the reached nodes
            reached_nodes = {
                node.state: node,
            }
            while pq.qsize() > 0:
                node = pq.get()[1]
                if node.state != start_pos:
                    # This list will be used to visualize the search
                    self.node_visited_list.append(node)
                # Return the current node if it is the goal
                if self.world.graph.graph[node.state[1]][node.state[0]].is_goal:
                    self._add_search_details("Astar search", start_time, node)
                    return node
                nodes: list[Node] = self.problem.expand(node, self.world.graph.graph)
                for i in range(len(nodes)):
                    # Add the node to pq if its state is not reached or if the state reached has a higher cost
                    if not nodes[i].state in reached_nodes or reached_nodes[nodes[i].state].path_cost > nodes[i].path_cost:
                        goal = self.closest_goal_to_cell(self.world.graph.graph[nodes[i].state[1]][nodes[i].state[0]])
                        distance_to_goal = manhatan(nodes[i], Node(state=goal.pos))
                        reached_nodes[nodes[i].state] = nodes[i]
                        pq.put((distance_to_goal + nodes[i].path_cost, nodes[i]))
        return None

    def reset_searches(self):
        self.node_visited_list = []
        self.node_visited_list_b = []
        self.search


    
    def IDS(self, start_pos):
        start_time = time.time()
        depth = 0
        #loop until the result is = None or a solution node
        if len(self.world.goals) == 0:return None
        while True:
            result = self.DLS(start_pos=start_pos, depth_limit=depth,start_time=start_time)
            if result != "CUTOFF": return result
            #increment depth limit
            depth += 1


    def DLS(self, start_pos, depth_limit, start_time):
        stack = deque()  
        node:Node = Node(state=start_pos)      
        stack.append(node)
        result = None
        while(len(stack) > 0): 
            node = stack.pop()
            self.node_visited_list.append(node)
            if(self.world.graph.graph[node.state[1]][node.state[0]].is_goal):
                self._add_search_details("Iterative deepening search", start_time, node)
                return node
            if node_depth(node) > depth_limit:
                #that means we will increase the depth in the next iteration of IDS.
                #There is still a chance that the solution can be found from any node in the stack if there is any.
                result = "CUTOFF"
            elif  not is_cycle(node=node):
                nodes = self.problem.expand(node, self.world.graph.graph)
                for i in range(len(nodes)-1, -1,-1):
                        stack.append(nodes[i])
            
        return result
    



    # def IDAstar(self, start_pos):
    #     start_time = time.time()
    #     node:Node = Node(start_pos)
    #     goal = self.closest_goal_to_cell(self.world.graph.graph[node.state[1]][node.state[0]])
    #     distacne_to_goal = self.world.graph.graph[node.state[1]][node.state[0]].manhatan(goal)
    #     threshold_limit = distacne_to_goal + node.path_cost
    #     fscores = [threshold_limit]
    #     while True:
    #         result = self.IDAsearch(node, start_time, fscores, goal)
    #         if result != "CUTOFF": return result
        

    # def IDAsearch(self, n:Node, start_time, fscores, goal):
        
    #     stack:deque = deque()
    #     stack.append(n)
    #     result = None
    #     limit = min(fscores)
    #     fscores.clear()
    #     while len(stack) > 0:
    #         node = stack.pop()
    #         #goal = self.closest_goal_to_cell(self.world.graph.graph[node.state[1]][node.state[0]])
    #         node_fscore = self.world.graph.graph[node.state[1]][node.state[0]].manhatan(goal) + node.path_cost
    #         if(self.world.graph.graph[node.state[1]][node.state[0]].is_goal):
    #             self._add_search_details("Iterative Deepening astar search", start_time=start_time, node = node)
    #             return node
    #         if(limit < node_fscore):
    #             result = "CUTOFF"
    #             fscores.append(node_fscore)
    #         elif not is_cycle(node):
    #             self.node_visited_list.append(node)
    #             nodes = self.__expandNodes(node=node)
    #             for i in range(len(nodes)-1, -1,-1):
    #                 stack.append(nodes[i])

    #     return result
    

    # def BBFS(self, start_pos):
    #     start_time = time.time()
    #     start_node:Node = Node(state=start_pos)

    #     closesest_goal = self.closest_goal_to_cell(self.world.graph.graph[start_pos[1]][start_pos[0]])
    #     if closesest_goal == None: return None
    #     goal_node:Node = Node(state=closesest_goal.pos)
    #     forward_q = deque()
    #     backward_q = deque()
    #     forward_q.append(start_node)
    #     backward_q.append(goal_node)
    #     f_reached = {start_node.state: start_node}
    #     b_reached = {goal_node.state: goal_node}
    #     solution = None
    #     while len(forward_q) > 0 and len(backward_q)> 0:
    #         solution = self.search("F", forward_q, f_reached, b_reached, solution, start_time,)
    #         solution = self.search("B", backward_q, b_reached, f_reached, solution, start_time, goal_node = goal_node)
    #         if solution != None:
    #             return solution

    #     return solution
    

    # def search(self, dir, frontier:deque, reached:list, reached_, solution, start_time, goal_node=Node(state=(0,0))):
    #     node = frontier.popleft()
    #     if dir == "F":
    #         self.node_visited_list.append(node)
    #     elif dir == "B":
    #         if node.state != goal_node.state:
    #             self.node_visited_list_b.append(node)

    #     nodes = self.__expandNodes(node)
    #     for child in nodes:
    #         if not child.state in reached:
    #             frontier.append(child)
    #             reached[child.state] = child
    #             if child.state in reached_:
    #                 if dir == "F":
    #                     self.node_visited_list_b.append(child)
    #                 elif dir == "B":
    #                     self.node_visited_list.append(child)
    #                 solution = self.join_nodes(child, reached_[child.state])
    #                 self._add_search_details("Bidirectional Breadth first search", start_time, solution)
    #                 return solution
                    
    #     return solution
    

    def BAstar(self, start_pos):
        start_time = time.time()
        start_node:Node = Node(state=start_pos)

        closesest_goal = self.closest_goal_to_cell(self.world.graph.graph[start_pos[1]][start_pos[0]])
        if closesest_goal == None: return None
        goal_node:Node = Node(state=closesest_goal.pos)
        forward_q = PriorityQueue()
        backward_q =PriorityQueue()
        #fScore_f = self.world.graph.graph[start_node.state[1]][start_node.state[0]].manhatan(closesest_goal) + start_node.path_cost
        #fScore_b = closesest_goal.manhatan(self.world.graph.graph[start_node.state[1]][start_node.state[0]]) + goal_node.path_cost
        fScore_f = manhatan(start_node, goal_node) + start_node.path_cost
        fScore_b = manhatan(goal_node, start_node) + goal_node.path_cost
        forward_q.put((fScore_f, start_node))
        backward_q.put((fScore_b, goal_node))
        f_reached = {start_node.state: start_node}
        b_reached = {goal_node.state: goal_node}
        solution = None
        while forward_q.qsize() > 0 and backward_q.qsize() > 0:
            solution = self.BAstarSearch("F", forward_q, f_reached, b_reached, solution,  goal_node, start_node)
            solution = self.BAstarSearch("B", backward_q, b_reached, f_reached, solution,  goal_node, start_node)

            # if (manhatan(forward_q.queue[0][1], goal_node) + forward_q.queue[0][1].path_cost) < (manhatan(backward_q.queue[0][1], start_node) + backward_q.queue[0][1].path_cost):
            #     solution = self.BAstarSearch("F", forward_q, f_reached, b_reached, solution,  goal_node, start_node)
            # else:
            #     solution = self.BAstarSearch("B", backward_q, b_reached, f_reached, solution,  goal_node, start_node)
            if solution != None:
                self._add_search_details("Bidirectional A* search", start_time, solution)
                return solution
        return solution
    

    def BAstarSearch(self, dir, frontier:PriorityQueue, reached:list, reached_, solution,  goal_node=Node(state=(0,0)), start_node =Node(state=(0,0))):
        node = frontier.get()[1]
        if dir == "F":
            self.node_visited_list.append(node)
        elif dir == "B":
            if node.state != goal_node.state:
                self.node_visited_list_b.append(node)
        nodes = self.problem.expand(node, self.world.graph.graph)
        for child in nodes:
            if not child.state in reached or reached[child.state].path_cost > child.path_cost:
                if dir == "F":
                    #fscore = self.world.graph.graph[child.state[1]][child.state[0]].manhatan(self.world.graph.graph[goal_node.state[1]][goal_node.state[0]]) + child.path_cost
                    fscore = manhatan(child, goal_node) + child.path_cost
                    frontier.put((fscore, child))
                elif dir == "B":
                    #fscore = self.world.graph.graph[child.state[1]][child.state[0]].manhatan(self.world.graph.graph[start_node.state[1]][start_node .state[0]]) + child.path_cost
                    fscore = manhatan(child, start_node) + child.path_cost
                    frontier.put((fscore, child))
                reached[child.state] = child
                solution2 = None
                if child.state in reached_:
                    if dir == "F":
                        self.node_visited_list_b.append(child)
                        solution2 = join_nodes(reached_[child.state], child)
                    elif dir == "B":
                        self.node_visited_list.append(child)
                        solution2 = join_nodes(child, reached_[child.state])
                        
                    #solution2 = join_nodes(child, reached_[child.state])
                    if solution != None:
                        if(solution2.path_cost < solution.path_cost):
                            solution = solution2
                    else:
                        solution = solution2
                    
        return solution
                


    
   

    #return the closest goal to the cell
    def closest_goal_to_cell(self, cell:Cell) -> Cell:
        #very big number
        closest_goal_dist = math.inf
        goal_cell:Cell = None
        #for row in range(self.world.graph.rows):
            # for col in range(self.world.graph.cols):
            #     if self.world.graph.graph[row][col].is_goal:
            #         #update the goal_cell with new goal distane if the current closest goal distance 
            #         # is bigger than the new measured goal distance.
            #         if (closest_goal_dist > cell.manhatan(self.world.graph.graph[row][col])):
            #             closest_goal_dist = cell.manhatan(self.world.graph.graph[row][col])
            #             goal_cell =  self.world.graph.graph[row][col]
        for goal in self.world.goals:
            if  closest_goal_dist > cell.manhatan(goal):
                closest_goal_dist =  cell.manhatan(goal)
                goal_cell = goal
        return goal_cell

    #return all the nodes that can be reached from the cureent node
    # def __expandNodes(self, node:Node):
    #     state = node.state
    #     nodes:list[Node] = []
    #     #return all the actions that can be applied on the current node state
    #     actions = action_applied_onStates(state, self.world.graph.graph)
    #     for key, value in actions.items():
    #         #apply action on the current state and return the new state
    #         s = actions[key](state)
    #         cost = node.path_cost + 1
    #         nodes.append(Node(state=s, parent=node, action = key, path_cost=cost))
    #     return nodes
    


    def _add_search_details(self, search_name, start_time, node):
        self.world.search_results = [
            search_name,
            #return the current time - the time the search started.
            "Real time take for search = " + str(float(round(time.time() - start_time, 6))),
            "Number of nodes visited = " + str(len(self.node_visited_list)+ len(self.node_visited_list_b)),
            "Path cost = " + str(get_path_cost(node=node))
        ]


    def reset_searches(self):
        self.node_visited_list.clear()
        self.node_visited_list_b.clear()
 
        
    

if __name__ == "__main__":
    node1 = Node((0,0))
    node2 = Node((0,0), node1)
    node3 = Node((0,0), node2)

    pq = PriorityQueue()
    pq.put(node1, 2)
    pq.put(node2, 1)
    print(pq.get())
    

#     print(node_depth(node3))


