import numpy as np
import random
import time
import heapq
from collections import deque

def print_maze(maze, path=None):
    if path:
        for x, y in path:
            if maze[x][y] not in ['S', 'G']:
                maze[x][y] = '*'
    print("\n".join(''.join(row) for row in maze))
    if path:
        for x, y in path:
            if maze[x][y] == '*':
                maze[x][y] = '.'

def generate_maze(size=10, obstacle_density=0.3):
    maze = np.full((size, size), '.')
    num_obstacles = int(size * size * obstacle_density)
    obstacles = set()
    while len(obstacles) < num_obstacles:
        obstacle = (random.randint(0, size-1), random.randint(0, size-1))
        obstacles.add(obstacle)
    for obstacle in obstacles:
        maze[obstacle] = 'X'
    start, goal = None, None
    while start == goal:
        start = (random.randint(0, size-1), random.randint(0, size-1))
        goal = (random.randint(0, size-1), random.randint(0, size-1))
        if start in obstacles or goal in obstacles or start == goal:
            start, goal = None, None
    maze[start] = 'S'
    maze[goal] = 'G'
    #print_maze(maze)
    return maze, start, goal

def dfs(maze, start, goal):
    start_time = time.time()
    stack = [(start, [start])]
    visited = set()
    nodes_expanded = 0
    while stack:
        (x, y), path = stack.pop()
        nodes_expanded += 1
        if (x, y) == goal:
            execution_time = time.time() - start_time
            print("\nDFS Results:")
            print("\nMaze Solution\n")
            print_maze(maze.copy(), path)
            return path, nodes_expanded, execution_time
        visited.add((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != 'X' and (nx, ny) not in visited:
                stack.append(((nx, ny), path + [(nx, ny)]))
    return None, nodes_expanded, time.time() - start_time

def bfs(maze, start, goal):
    start_time = time.time()
    queue = deque([(start, [start])])
    visited = set()
    nodes_expanded = 0
    while queue:
        (x, y), path = queue.popleft()
        nodes_expanded += 1
        if (x, y) == goal:
            execution_time = time.time() - start_time
            print("\nBFS Results:")
            print("\nMaze Solution\n")
            print_maze(maze.copy(), path)
            return path, nodes_expanded, execution_time
        visited.add((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != 'X' and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
    return None, nodes_expanded, time.time() - start_time

def a_star(maze, start, goal):
    start_time = time.time()
    queue = [(0 + heuristic(start, goal), 0, start, [start])]
    visited = set()
    nodes_expanded = 0
    while queue:
        _, cost, (x, y), path = heapq.heappop(queue)
        nodes_expanded += 1
        if (x, y) == goal:
            execution_time = time.time() - start_time
            print("\nA* Results:")
            print("\nMaze Solution\n")
            print_maze(maze.copy(), path)
            return path, nodes_expanded, execution_time
        visited.add((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != 'X' and (nx, ny) not in visited:
                new_cost = cost + 1
                heapq.heappush(queue, (new_cost + heuristic((nx, ny), goal), new_cost, (nx, ny), path + [(nx, ny)]))
    return None, nodes_expanded, time.time() - start_time

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def run_all_algorithms_on_same_maze(algorithms, size=10, obstacle_density=0.3, runs=10):
    avg_results = {name: {"path_length": [], "nodes_expanded": [], "execution_time": [], "pass_count": 0} for name in algorithms.keys()}
    
    for run in range(1,runs + 1):
        maze, start, goal = generate_maze(size, obstacle_density)
        print(f"\nRun {run} Maze:")
        print_maze(maze)
        #performance for each run
        for name, algorithm in algorithms.items():
            path, nodes_expanded, execution_time = algorithm(maze, start, goal)
            path_length = len(path) if path else 0
            pass_status = "Pass" if path_length > 0 else "Fail"
            #for successful runs
            avg_results[name]["nodes_expanded"].append(nodes_expanded)
            avg_results[name]["execution_time"].append(execution_time)
            if path_length > 0:
                avg_results[name]["pass_count"] += 1
                avg_results[name]["path_length"].append(path_length)
            
            #printed results for each run
            print(f"\n{name} - Status: {pass_status}, Path Length: {path_length}, Nodes Expanded: {nodes_expanded}, Execution Time: {execution_time:.5f} seconds")


    # print average results for successful runs only
    print("*****************************")
    print("\nAverage Results For Successful Runs:\n")
    for name, performance in avg_results.items():
        if performance["pass_count"] > 0:  
            avg_sol_path_length = np.mean(performance["path_length"])
            avg_nodes_expanded = np.mean(performance["nodes_expanded"])
            avg_execution_time = np.mean(performance["execution_time"])
        
        print(f"{name}: Total Successes = {performance['pass_count']}, Average Solution Path Length = {avg_sol_path_length}, Average Nodes Expanded = {avg_nodes_expanded}, Average Execution Time = {avg_execution_time:5f}\n")



algorithms = {"DFS": dfs, "BFS": bfs, "A*": a_star}
run_all_algorithms_on_same_maze(algorithms)


#visualization for algorithms

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def generate_maze(size=10, obstacle_density=0.3):
    maze = np.full((size, size), 0) 
    num_obstacles = int(size**2 * obstacle_density)
    for _ in range(num_obstacles):
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        maze[x, y] = 1  
    start, goal = (0, 0), (size-1, size-1) 
    maze[start] = 2 
    maze[goal] = 3 
    return maze, start, goal

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def dfs(maze, start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        (x, y), path = stack.pop()
        visited.add((x, y))
        yield path
        if (x, y) == goal:
            return
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and maze[nx, ny] != 1 and (nx, ny) not in visited:
                stack.append(((nx, ny), path + [(nx, ny)]))

def bfs(maze, start, goal):
    queue = deque([([start], start)])
    visited = set([start])
    while queue:
        path, (x, y) = queue.popleft()
        yield path
        if (x, y) == goal:
            return
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx, ny] != 1 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((path + [(nx, ny)], (nx, ny)))

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def a_star(maze, start, goal):
    queue = [(0 + heuristic(start, goal), 0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    visited = set()

    while queue:
        _, cost, current = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        yield reconstruct_path(came_from, current)

        if current == goal:
            return  

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and maze[nx, ny] != 1 and (nx, ny) not in visited:
                new_cost = cost_so_far[current] + 1
                if (nx,ny) not in cost_so_far or new_cost < cost_so_far[nx, ny]:
                    cost_so_far[nx, ny] = new_cost
                    priority = new_cost + heuristic((nx, ny), goal)
                    heapq.heappush(queue, (priority, new_cost, (nx, ny)))
                    came_from[nx, ny] = current


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def run_and_animate_algorithm(maze, algorithm, title):
    maze_visual = np.copy(maze)  

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_title(title)

    def update(path):
        ax.clear()
        ax.set_title(title)
        temporary_maze = np.copy(maze_visual)
        for x, y in path:
            if temporary_maze[x, y] != 2 and temporary_maze[x, y] != 3: 
                temporary_maze[x, y] = 4  
        ax.imshow(temporary_maze, cmap='viridis')
        ax.axis('off')

    ani = FuncAnimation(fig, update, frames=algorithm(maze, start, goal), repeat=False,cache_frame_data=False)
    plt.show()

maze, start, goal = generate_maze()

for algorithm, title in [(dfs, "DFS Maze Solution"), (bfs, "BFS Maze Solution"), (a_star, "A* Maze Solution")]:
    run_and_animate_algorithm(maze, algorithm, title)

