import os
import matplotlib.pyplot as plt
from collections import Counter, defaultdict, deque
from queue import PriorityQueue

print("[1] Matrix with Height = 11 and Width = 22\n")
print("[2] Matrix with Height = 11 and Width = 27\n")
print("[3] Matrix with Height = 15 and Width = 27\n")
print("[4] Matrix with Height = 18 and Width = 30\n")
print("[5] Matrix with Height = 32 and Width = 35\n")
maze = ''
choice = int(input("Enter your choice:\t"))
if choice == 1:
  maze = 'maze_map1.txt'
elif choice == 2:
  maze = 'maze_map2.txt'
elif choice == 3:
  maze = 'maze_map3.txt'
elif choice == 4:
  maze = 'maze_map4.txt'
elif choice == 5: 
  maze = 'maze_map5.txt'      
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

DIR = [0, 1, 0, -1, 0]

def neighbors(pos):
    for i in range(4):
        n_r, n_c = pos[0] + DIR[i], pos[1] + DIR[i+1]
        if n_r < 0 or n_c < 0 or n_r >= len(matrix) or n_c >= len(matrix[0]) or matrix[n_r][n_c] == 'x': continue
        yield (n_r,n_c)

def dfs(PosS,Exit):
    seen = set()
    seen.add(PosS)
    track = {} #Tạo dict để chứa các đường đi đã thử của thuật toán
    def _DFS(pos): # Chạy đệ qui DFS
        for nei in neighbors(pos): # Các điểm có thể đi đến được từ điểm hiện tại
            if nei not in seen: # Nếu chưa đi qua điểm này
                seen.add(nei) # Lưu lại dấu vết
                track[nei] = (pos)
                if nei == Exit:
                    return True  
                elif _DFS(nei): #Đệ qui lại hàm
                    return True
        return False

    if (_DFS(PosS)):
        pos = Exit
        list_route = []
        while pos in track:
            list_route.append(pos)
            pos = track[pos]
        return list_route[::-1]
    return None
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

heuristic = {}
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        pos = (i,j)
        heuristic[pos] = abs(i - end[0]) + abs(j - end[1])

Grid = set()
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        Grid.add((i,j))

#Thuật toán GBFS
def GBFS(PosS, Exit):
    f_score = {cell:float('inf') for cell in Grid}
    f_score[PosS] = heuristic[PosS]

    open = PriorityQueue()
    open.put((heuristic[PosS],PosS))
    aPath = {}
    
    while not open.empty():
        currCell = open.get()[1]
        if(currCell == Exit):
            break
        for nei in neighbors(currCell):
            temp_f_s = heuristic[nei] 
            if(temp_f_s < f_score[nei]):
                f_score[nei] = temp_f_s
                open.put((heuristic[nei],nei))
                aPath[nei] = (currCell)
    list_route = []
    pos = Exit
    while pos != PosS:
        list_route.append(pos)
        pos = aPath[pos]
    return list_route[::-1]

#Thuật toán A*
def AStar(PosS, Exit):
    g_score = {cell:float('inf') for cell in Grid}
    g_score[PosS] = 0
    f_score = {cell:float('inf') for cell in Grid}
    f_score[PosS] = heuristic[PosS]

    open = PriorityQueue()
    open.put((heuristic[PosS],heuristic[PosS],PosS))
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
                aPath[nei] = (currCell)
    list_route = []
    pos = Exit
    while pos != PosS:
        list_route.append(pos)
        pos = aPath[pos]
    return list_route[::-1]

print("\n[1] Run with DFS\n")
print("[2] Run with BFS\n")
print("[3] Run with GBFS\n")
print("[4] Run with A*\n")
choice_A = int(input("Enter your choice:\t"))
if choice_A == 1:
  route = dfs(start,end)
  route.insert(0,start)
elif choice_A == 2:
  route = bfs(start,end)
  route.insert(0,start)
elif choice_A == 3:
  route = GBFS(start,end)
  route.insert(0,start)
elif choice_A == 4:
  route = AStar(start,end)
  route.insert(0,start)
else:
  print("Invalid choice\n")

visualize_maze(matrix,bonus_points,start,end,route)