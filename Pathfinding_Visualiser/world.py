from collections import deque
import pygame
import threading
import time
import _thread
from graph import*

class World:
    def __init__(self, file_name, width=770, height=650) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(size=(width, height))
        self.font = pygame.font.SysFont(None, 24)
        self.file_name = file_name
        self.width = width
        self.height = height
        self.agent_start_pos = None
        self.goals = []
        self.graph = self.__readMapFile(file_name=file_name)
        #self.graph_graph_copy = []
        #self.graph_graph_copy.extend(self.graph.graph)
        self.rect = self.__initRect()
        self.path = []
        self.running= True
        self.counter = 0
        self.visited_nodes = []
        self.agent_current_cell:Cell = None
        self.dbClick =  pygame.time.Clock()
        self.search_results = []
        self.event_time_counter = 40
       
        


        


    def clear_world(self):
        self.visited_nodes.clear()
        self.path.clear()
        for row in range(len(self.graph.graph)):
            for col in range(len(self.graph.graph[0])):
                if(self.graph.graph[row][col].is_visited):
                    self.graph.graph[row][col].is_visited = False
                    self.agent_current_cell = None
                   

    def reset_world(self):
        self.graph = self.__readMapFile(self.file_name)
       

    def render(self):
        self.screen.fill('white')
        self.__draw_grid()
        self.__draw_path()
        self.draw_solution_details()
        #self.intro_menu(screen=surface)




    def set_cell_visited(self, nodes_visited:list[Node], nodes_visited2:list[Node]):
        if(len(nodes_visited) != 0):
            node:Node = nodes_visited.pop(0)
            #this is the node that will be expanded
            self.agent_current_cell = self.graph.graph[node.state[1]][node.state[0]]
            if(node.state != self.agent_start_pos):
                #setting the cell to visited will and this cell will be drawen in the render function with new color
                self.graph.graph[node.state[1]][node.state[0]].is_visited = True

        if(len(nodes_visited2) != 0):
            node:Node = nodes_visited2.pop(0)
            #setting the cell to visited will and this cell will be drawen in the render function with new color
            self.graph.graph[node.state[1]][node.state[0]].is_visited = True
        
        

        


    def add_visited_nodes(self):
        for row in range(self.graph.rows):
            for col in range(self.graph.cols):
                if (self.graph.graph[row][col].is_visited):
                    self.visited_nodes.append(self.graph.graph[row][col])

   

    def __initRect(self):
        rects =[[pygame.Rect(0.0, 0.0 ,0, 0) for i in range(len(self.graph.graph[0]))] for j in range(len(self.graph.graph))]
        rect_width = round(self.width/(len(self.graph.graph[0])))
        rect_height = round((self.height-150)/(len(self.graph.graph)))
        rect_x:float = 0.0
        rect_y:float = 0.0

        for row in range(len(self.graph.graph)):
            for col in range(len(self.graph.graph[0])):
                rects[row][col] = pygame.Rect(float(rect_x), float(rect_y), float(rect_width), float(rect_height))
                self.graph.graph[row][col].cart_pos = (rect_x, rect_y)
                rect_x += rect_width
            rect_x = 0.0
            rect_y += rect_height
            
        
        return rects
    



    def draw_solution_details(self):
        height = 500
        for i in range(len(self.search_results)):
           height += 20
           text_surface = self.font.render(str(self.search_results[i]), True, "black")
           self.screen.blit(text_surface, (50, height))


    def __draw_path(self):
        for i in range(1, len(self.path)-1, 1):
           pygame.draw.rect(self.screen, "yellow", self.rect[self.path[i][1]][self.path[i][0]])
           pygame.draw.rect(self.screen, "black", self.rect[self.path[i][1]][self.path[i][0]], width=1)
    
    # def get_path_cost(self, node:Node):
    #     while(node != None):
    #             print(node.action)
    #             #world.path.append((world.rect[node.state[1]][node.state[0]].left, world.rect[node.state[1]][node.state[0]].top))
    #             self.path.append(node.state)
    #             node = node.parent


    def __draw_grid(self):
        pygame.draw.rect(self.screen, "red", pygame.Rect(self.rect[self.agent_start_pos[1]][self.agent_start_pos[0]].left, self.rect[self.agent_start_pos[1]][self.agent_start_pos[0]].top, self.rect[self.agent_start_pos[1]][self.agent_start_pos[0]].width, self.rect[self.agent_start_pos[1]][self.agent_start_pos[0]].height ))
        for row in range(len(self.graph.graph)):
            for col in range(len(self.graph.graph[0])):

                if(self.graph.graph[row][col].is_wall):
                    pygame.draw.rect(self.screen, "dark grey", self.rect[row][col], width=0)
                    pygame.draw.rect(self.screen, "black", self.rect[row][col], width=1)
                elif(self.graph.graph[row][col].is_goal):
                    pygame.draw.rect(self.screen, "green", self.rect[row][col])
                    pygame.draw.rect(self.screen, "black", self.rect[row][col], width=1)
                else:
                    pygame.draw.rect(self.screen, "black", self.rect[row][col], width=1)
                if(self.graph.graph[row][col].is_visited):
                    pygame.draw.rect(self.screen, (114,194,255), self.rect[row][col], width=0)
                    pygame.draw.rect(self.screen, "black", self.rect[row][col], width=1)
                if(self.graph.graph[row][col].is_in_frontier):
                     pygame.draw.rect(self.screen, "blue", self.rect[row][col], width=0)
                     pygame.draw.rect(self.screen, "black", self.rect[row][col], width=1)
        if(self.agent_current_cell != None):
            pygame.draw.rect(self.screen, (246,172,0), self.rect[self.agent_current_cell.pos[1]][self.agent_current_cell.pos[0]], width=0)
            pygame.draw.rect(self.screen, "black", self.rect[self.agent_current_cell.pos[1]][self.agent_current_cell.pos[0]], width=1)




    def __add_remove_goal(self):
         #mouse_pressed = pygame.mouse.get_pressed()
         #if mouse_pressed[2]:
            #if self.dbClick.tick() < 500:
        for row in range(self.graph.rows):
            for col in range(self.graph.cols):
                if pygame.mouse.get_pos()[0] > self.rect[row][col].left and pygame.mouse.get_pos()[0] < (self.rect[row][col].left + self.rect[row][col].width) and pygame.mouse.get_pos()[1] > self.rect[row][col].top and pygame.mouse.get_pos()[1] <(self.rect[row][col].top + self.rect[row][col].height):
                    if (not self.graph.graph[row][col].is_goal and not self.graph.graph[row][col].is_wall):
                        self.graph.graph[row][col].is_goal = True
                        self.goals.append(self.graph.graph[row][col])
                        return
                    if (not self.graph.graph[row][col].is_wall):
                        self.goals.remove(self.graph.graph[row][col])
                        self.graph.graph[row][col].is_goal = False


    def __remove_add_wall(self,):
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            mouse = self.is_mouse_in_cell()
            if(mouse[0]):
                if not self.graph.graph[mouse[1]][mouse[2]].is_goal:
                    self.graph.graph[mouse[1]][mouse[2]].is_wall = True
        elif mouse_pressed[2]:
            mouse = self.is_mouse_in_cell()
            if mouse[0]:
                self.graph.graph[mouse[1]][mouse[2]].is_wall = False

                

    def event_handler(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            self.clear_world()
        if (self.event_time_counter > 30):
            self.event_time_counter =0
            if keys[pygame.K_w]:
                self.__add_remove_goal()
        if keys[pygame.K_r]:
            self.reset_world()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running == False
            self.__remove_add_wall()
            #to add or remove goal press t and click on the cell by the mouse
        self.__remove_add_wall()
        self.event_time_counter += 1


    def intro_menu(self, screen):

        pygame.draw.rect(screen, "white", pygame.Rect(50, 50, 400, 400))
        font = pygame.font.Font(None, 40)
        font_surface = font.render("Press A to start A* search, B for Breadth first search, \nG for Greedy Best first search, D for depth first search", False, (0,0,0))
        font_pos = font_surface.get_rect(center = (350, 300))
        screen.blit(font_surface, font_pos)


    def is_mouse_in_cell(self):
        for row in range(len(self.graph.graph)):
            for col in range(len(self.graph.graph[0])):
                if pygame.mouse.get_pos()[0] > self.rect[row][col].left and pygame.mouse.get_pos()[0] < (self.rect[row][col].left + self.rect[row][col].width) and pygame.mouse.get_pos()[1] > self.rect[row][col].top and pygame.mouse.get_pos()[1] <(self.rect[row][col].top + self.rect[row][col].height):
                    return (True,row,col)
        return (False,0,0)
    

   
    def __readMapFile(self,file_name):
        graph = None
        file = open(file_name, "r")
        file_content = file.readlines()
        line_num = 0
        for line in file_content:
            if(line_num == 0):
                numbers = [int(n) for n in line.strip()[1:-1].split(",")]
                graph = Graph(numbers[0], numbers[1])
            if line_num == 1:
                initialPos = [int(n) for n in line.strip()[1:-1].split(",")]
                self.agent_start_pos = (initialPos[0], initialPos[1])
            if line_num == 2:
                goals_pos = [n for n in line.strip().split("|")]
                self.goals.clear()
                for p in goals_pos:
                    pos = p.strip()[1:-1].split(",")
                    if len(pos) == 2:
                        graph.graph[int(pos[1])][int(pos[0])].is_goal = True
                        self.goals.append(graph.graph[int(pos[1])][int(pos[0])])
            if  line_num == 3:
                wall_cell = [int(n) for n in line.strip()[1:-1].split(",")]
                graph.graph[wall_cell[1]][wall_cell[0]].is_wall = True
                if(wall_cell[2] > 1): #the width of the wall
                    for i in range(wall_cell[2]):
                        graph.graph[wall_cell[1]][wall_cell[0]+i].is_wall = True
                if wall_cell[3] > 1: #the height of the wall
                    for i in range(1, wall_cell[3]):
                        for j in range(wall_cell[2]):
                            graph.graph[wall_cell[1]+i][wall_cell[0] + j].is_wall =True
            if line_num != 3:
                line_num+=1
        return graph


