from collections import Counter, defaultdict, deque
from queue import PriorityQueue


DIR = [0, 1, 0, -1, 0]

def neighbors(pos):
    for i in range(4):
        n_r, n_c = pos[0] + DIR[i], pos[1] + DIR[i+1]
        if n_r < 0 or n_c < 0 or n_r >= len(matrix) or n_c >= len(matrix[0]) or matrix[n_r][n_c] == 'x': continue
        yield (n_r,n_c)

#Thuật toán DFS
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
        while pos in track: #Lấy ra đường đi
            list_route.append(pos)
            pos = track[pos]
        return list_route[::-1]
    return None
#Thuật toán BFS
def bfs(PosS,Exit):
    q = deque([PosS])
    seen = set()
    seen.add(PosS)
    track = {} #Tạo dict để chứa các đường đi đã thử của thuật toán
    while q:
        for _ in range(len(q)):
            pos = q.popleft() #Lấy phần tử đầu tiên ra để xét
            if pos == Exit:
                list_route = []
                while pos in track:
                    list_route.append(pos)
                    pos = track[pos]
                return list_route[::-1]
            for nei in neighbors(pos): #Kiểm tra các điểm xung quanh
                if nei not in seen: #Nếu chưa đi thì thêm vào hàng đợi
                    track[nei] = (pos)
                    seen.add(nei)
                    q.append(nei)

heuristic = {}  #Công thức heuristic tại mọi điểm
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        pos = (i,j)
        heuristic[pos] = abs(i - end[0]) + abs(j - end[1]) #Là chi phí từ điểm đó tới Exit mà k có tường ngăn cản

Grid = set()  #Tạo set lưu tất cả các điểm của mê cung
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        Grid.add((i,j))

#Thuật toán GBFS
def GBFS(PosS, Exit):
    f_score = {cell:float('inf') for cell in Grid}
    f_score[PosS] = heuristic[PosS] #Lưu giá trị Heuristic vào từng vị trí

    open = PriorityQueue() #Sử dụng hàng đợi ưu tiên để lấy được đường có chi phí thấp nhất
    open.put((heuristic[PosS],PosS))
    aPath = {}
    
    while not open.empty(): 
        currCell = open.get()[1]
        if(currCell == Exit):
            break
        for nei in neighbors(currCell):
            temp_f_s = heuristic[nei] #Chỉ tính giá trị của f(x)
            if(temp_f_s < f_score[nei]): #Nếu chi phí nào nhỏ hơn thì sẽ lưu giá trị đó vào hàng đợi ưu tiên
                f_score[nei] = temp_f_s
                open.put((heuristic[nei],nei))
                aPath[nei] = (currCell)
    list_route = []
    pos = Exit
    while pos != PosS: #Sử dụng để lấy ra đường đi ngắn nhất
        list_route.append(pos)
        pos = aPath[pos]
    return list_route[::-1]

#Thuật toán A*
def AStar(PosS, Exit):
    g_score = {cell:float('inf') for cell in Grid} # Lưu giá trị đã đi vào từng vị trí
    g_score[PosS] = 0  #g(x)
    f_score = {cell:float('inf') for cell in Grid} #Lưu giá trị Heuristic vào từng vị trí
    f_score[PosS] = heuristic[PosS] #f(x)

    open = PriorityQueue() #Sử dụng hàng đợi ưu tiên để lấy được đường có chi phí thấp nhất
    open.put((heuristic[PosS],heuristic[PosS],PosS))
    aPath = {}

    while not open.empty():
        currCell = open.get()[2]
        if(currCell == Exit):
            break
        for nei in neighbors(currCell):
            temp_g_s = g_score[currCell] + 1 # Tăng giá trị chi phí đường đi hiện tại
            temp_f_s = temp_g_s + heuristic[nei]  #Tổng giá trị f(x) và g(x)
            if(temp_f_s < f_score[nei]): #Nếu chi phí nào nhỏ hơn thì sẽ lưu giá trị đó vào hàng đợi ưu tiên
                g_score[nei] = temp_g_s
                f_score[nei] = temp_f_s
                open.put((temp_f_s,heuristic[nei],nei))
                aPath[nei] = (currCell)
    list_route = []
    pos = Exit
    while pos != PosS: #Sử dụng để lấy ra đường đi ngắn nhất
        list_route.append(pos)
        pos = aPath[pos]
    return list_route[::-1]


    #Thuật toán tìm kiếm với điểm thưởng
    def AStar_P(PosS, Exit): #Dùng để kiểm tra chi phí tới điểm đó tương tự như A*
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

def theNearest(PosS): #Kiểm tra điểm thưởng gần đó nhất
    index = 0
    if(len(PlusP) == 1):
        return 0
    pos = PlusP[index]
    val = plusVal[index]
    for i in range(len(PlusP)):
        if AStar_P(PosS,PlusP[index])[1] + plusVal[index] > AStar_P(PosS,PlusP[i])[1] + plusVal[i]:
            index = i
    return index 

def PLusPoint(PosS, Exit): #Hàm chính để đưa ra đường đi
    route = []
    index = theNearest(PosS)
    now_p = PosS
    while True:
        pos = PlusP[index]
        val = plusVal[index]
        if AStar_P(now_p,pos)[1] + AStar_P(pos,Exit)[1] + val < AStar_P(now_p, Exit)[1]: #So sánh đường đi mới có tối ưu không
            route += bfs(now_p,pos) #Nếu có thì thêm vào route
            now_p = PlusP[index] #Đổi điểm hiện tại sang điểm thưởng mới này
        if(len(PlusP) == 1): #Nếu không còn điểm thưởng thì công thêm đường đi tới Exit
            route += bfs(now_p,Exit)
            return route
        PlusP.pop(index)
        plusVal.pop(index)
        index = theNearest(now_p)

# Thuật toán khi có cổng dịch chuyển
def neighbors(pos): # Định nghĩa là hàm neighbors do có cổng dịch chuyển nên nó không còn giống hàm cũ nữa
    for i in range(4):
        n_r, n_c = pos[0] + DIR[i], pos[1] + DIR[i+1]
        if n_r < 0 or n_c < 0 or n_r >= len(matrix) or n_c >= len(matrix[0]): continue
        if matrix[n_r][n_c] == 'x': continue
        if (n_r,n_c) in Gate.keys():
            n_r,n_c = Gate[(n_r,n_c)]
        yield (n_r,n_c)

def TeletheNearest(PosS): #Tìm kiếm đường ngắn nhất đi tới 1 trong các điểm thưởng 
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
        if len(bfs(now_p,pos)) + len(bfs(pos,Exit)) + val < len(bfs(now_p, Exit)): #Kiểm tra đi qua điểm thưởng có tối ưu không
            route += bfs(now_p,pos)
            now_p = PlusP[index]
        if(len(PlusP) == 1):
            route += bfs(now_p,Exit) #Tương tự như điểm thưởng
            return route
        PlusP.pop(index)
        plusVal.pop(index)
        index = TeletheNearest(now_p)