import math

class Cell:
    def __init__(self, pos = (0,0)) -> None:
       self.cart_pos:tuple[int, int] = (0,0)
       self.is_wall = False
       self.pos = pos #(x, y) 
       self.is_goal =  False
       self.is_visited = False
       self.is_in_frontier = False
    
    def hypot(self, other):
        return math.sqrt((other.cart_pos[0] - self.cart_pos[0])**2 + (other.cart_pos[1]-self.cart_pos[1])**2)
    
    def manhatan(self, other):
        return (abs(self.pos[0] - other.pos[0]) + abs(self.pos[1] - other.pos[1]))
                    
