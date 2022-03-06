import os
import matplotlib.pyplot as plt
from collections import Counter, defaultdict, deque
from queue import PriorityQueue


print("[1] Matrix with Height = 11 and Width = 22\n")
print("[2] Matrix with Height = 15 and Width = 27\n")
print("[3] Matrix with Height = 32 and Width = 35\n")
maze = ''
choice = int(input("Enter your choice:\t"))
if choice == 1:
  maze = 'maze_map1.txt'
elif choice == 2:
  maze = 'maze_map2.txt'
elif choice == 3:
  maze = 'maze_map3.txt'
else:
  print("Invalid choice\n")

def visualize_maze(matrix, bonus, start, end, gate = None, route=None):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']

    if route:
        direction=[]
        for i in range(1,len(route)):
            if route[i][0]-route[i-1][0]>0:
                direction.append('v') #^
            elif route[i][0]-route[i-1][0]<0:
                direction.append('^') #v        
            elif route[i][1]-route[i-1][1]>0:
                direction.append('>')
            else:
                direction.append('<')

        direction.pop(0)
    if gate:
        Gate_in = list(gate.keys())
        Gate_out = list(gate.values())
    #2. Drawing the map
    ax=plt.figure(dpi=100,figsize=(10,6)).add_subplot(111)

    for i in ['top','bottom','right','left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls],[-i[0] for i in walls],
                marker='X',s=100,color='black')
    
    plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                marker='P',s=100,color='green')

    plt.scatter(start[1],-start[0],marker='*',
                s=100,color='gold')
    
    if gate:
        plt.scatter([i[1] for i in Gate_in],[-i[0] for i in Gate_in],
                marker='o',s=100,color='purple')
        plt.scatter([i[1] for i in Gate_out],[-i[0] for i in Gate_out],
                marker='h',s=100,color='pink')
        
    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1],-route[i+1][0],
                        marker=direction[i],color='silver')

    plt.text(end[1],-end[0],'EXIT',color='red',
         horizontalalignment='center',
         verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')
    print()
    for _, point in enumerate(bonus):
      print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')
    print()
    for _, point in enumerate(Gate_in):
      print(f'Gate_in point at position (x, y) = {point[0], point[1]} with Gate_out {gate[(point[0], point[1])]}')

def read_file_teleport(file_name: str = 'maze.txt'):
  f=open(file_name,'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = []
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))
  
  n_gate_points = int(next(f)[:-1])
  Gate_tele = {}
  for j in range(n_gate_points):
    x, y, z, t = map(int, next(f)[:-1].split(' '))
    Gate_tele[(x,y)] = (z,t)
    
  text=f.read()
  matrix=[list(i) for i in text.splitlines()]
  f.close()

  return bonus_points, Gate_tele, matrix

bonus_points, Gate, matrix = read_file_teleport(maze)
for i in range(len(matrix)):
  for j in range(len(matrix[0])):
    if matrix[i][j]=='S':
      start=(i,j)

    elif matrix[i][j]==' ':
      if (i==0) or (i==len(matrix)-1) or (j==0) or (j==len(matrix[0])-1):
        end=(i,j)
                
      else:
        pass
PlusP = []
plusVal = []
for i in range(len(bonus_points)):
    PlusP.append((bonus_points[i][0],bonus_points[i][1]))
    plusVal.append(bonus_points[i][2])
DIR = [0, 1, 0, -1, 0]

def neighbors(pos):
    for i in range(4):
        n_r, n_c = pos[0] + DIR[i], pos[1] + DIR[i+1]
        if n_r < 0 or n_c < 0 or n_r >= len(matrix) or n_c >= len(matrix[0]): continue
        if matrix[n_r][n_c] == 'x': continue
        if (n_r,n_c) in Gate.keys():
            n_r,n_c = Gate[(n_r,n_c)]
        yield (n_r,n_c)

#Thuật toán BFS
def bfs(PosS,Exit):
    q = deque([PosS])
    seen = set()
    seen.add(PosS)
    track = {}
    while q:
        for _ in range(len(q)):
            pos = q.popleft()
            if pos == Exit:
                list_route = []
                while pos in track:
                    list_route.append(pos)
                    pos = track[pos]
                return list_route[::-1]
            for nei in neighbors(pos):
                if nei not in seen:
                    track[nei] = (pos)
                    seen.add(nei)
                    q.append(nei)

def TeletheNearest(PosS):
    index = 0
    if(len(PlusP) == 1):
        return 0
    pos = PlusP[index]
    val = plusVal[index]
    for i in range(len(PlusP)):
        if len(bfs(PosS,PlusP[index])) + plusVal[index] > len(bfs(PosS,PlusP[i])) + plusVal[i]:
            index = i
    return index     

def TeleP(PosS, Exit):
    route = []
    index = TeletheNearest(PosS)
    now_p = PosS
    while True:
        pos = PlusP[index]
        val = plusVal[index]
        if len(bfs(now_p,pos)) + len(bfs(pos,Exit)) + val < len(bfs(now_p, Exit)):
            route += bfs(now_p,pos)
            now_p = PlusP[index]
        if(len(PlusP) == 1):
            route += bfs(now_p,Exit)
            return route
        PlusP.pop(index)
        plusVal.pop(index)
        index = TeletheNearest(now_p)

route = TeleP(start,end) #
route.insert(0,start)
for val in Gate.values():
    if val in route:
        for key in Gate.keys():
            if Gate[key] == val:
                route[route.index(val)] = key

visualize_maze(matrix,bonus_points,start,end,Gate,route)