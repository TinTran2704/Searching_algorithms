import os
import sys
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

def visualize_maze(matrix, bonus, start, end, route=None):
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
    
    for _, point in enumerate(bonus):
      print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')

def read_file(file_name: str = 'maze.txt'):
  f=open(file_name,'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = []
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))

  text=f.read()
  matrix=[list(i) for i in text.splitlines()]
  f.close()

  return bonus_points, matrix

bonus_points, matrix = read_file(maze)
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
        if n_r < 0 or n_c < 0 or n_r >= len(matrix) or n_c >= len(matrix[0]) or matrix[n_r][n_c] == 'x': continue
        yield (n_r,n_c)

heuristic = {}
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        pos = (i,j)
        heuristic[pos] = abs(i - end[0]) + abs(j - end[1])

Grid = set()
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        Grid.add((i,j))

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

def AStar_P(PosS, Exit):
    g_score = {cell:float('inf') for cell in Grid}
    g_score[PosS] = 0
    f_score = {cell:float('inf') for cell in Grid}
    f_score[PosS] = heuristic[PosS]

    open = PriorityQueue()
    open.put((heuristic[PosS],heuristic[PosS],PosS))  #Tại ban đầu thi chip phí G(x) = 0
    aPath = {}

    while not open.empty():
        currCell = open.get()[2]
        if(currCell == Exit):
            break
        for nei in neighbors(currCell): 
            temp_g_s = g_score[currCell] + 1
            temp_f_s = temp_g_s + heuristic[nei]
            if(temp_f_s < f_score[nei]):
                g_score[nei] = temp_g_s
                f_score[nei] = temp_f_s
                open.put((temp_f_s,heuristic[nei],nei))
                aPath[nei] = (currCell,temp_g_s)
    return aPath[Exit]

def theNearest(PosS):
    index = 0
    if(len(PlusP) == 1):
        return 0
    pos = PlusP[index]
    val = plusVal[index]
    for i in range(len(PlusP)):
        if AStar_P(PosS,PlusP[index])[1] + plusVal[index] > AStar_P(PosS,PlusP[i])[1] + plusVal[i]:
            index = i
    return index 

def PLusPoint(PosS, Exit):
    route = []
    index = theNearest(PosS)
    now_p = PosS
    while True:
        pos = PlusP[index]
        val = plusVal[index]
        if AStar_P(now_p,pos)[1] + AStar_P(pos,Exit)[1] + val < AStar_P(now_p, Exit)[1]:
            route += bfs(now_p,pos)
            now_p = PlusP[index]
        if(len(PlusP) == 1):
            route += bfs(now_p,Exit)
            return route
        PlusP.pop(index)
        plusVal.pop(index)
        index = theNearest(now_p)

route = PLusPoint(start,end)
route.insert(0,start)

visualize_maze(matrix,bonus_points,start,end,route)