import pygame
import random
import time
import heapq

scr_width = 800
scr_height = 600

mze_width = 40
mze_height = 30
rect_size = 20

directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

pygame.init()

size = [scr_width, scr_height]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("A* Pathfinding Visualizer")

done = False
clock = pygame.time.Clock()

# Maze generator function, just generates the list of tiles, doesn't draw anything
# Reference I used: https://aryanab.medium.com/maze-generation-recursive-backtracking-5981bc5cc766
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    start = (0, 0)
    stack = [start]

    while stack:
        current = stack[-1]
        x, y = current
        maze[y][x] = 0
        neighbors = []

        for direction in directions:
            nx, ny = x + direction[0] * 2, y + direction[1] * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                neighbors.append((nx, ny))

        if neighbors:
            next_cell = random.choice(neighbors)
            nx, ny = next_cell
            maze[(y + ny) // 2][(x + nx) // 2] = 0
            stack.append(next_cell)
        else:
            stack.pop()

    return maze

def draw_maze(maze, player_pos):
    for y in range(mze_height):
        for x in range(mze_width):
            color = (255, 255, 255) if maze[y][x] == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, [x * rect_size, y * rect_size, rect_size, rect_size])

    pygame.draw.rect(screen, (0, 255, 0), [0, 0, rect_size, rect_size])
    pygame.draw.rect(screen, (255, 0, 0), [(mze_width - 2) * rect_size, (mze_height - 2) * rect_size, rect_size, rect_size])

    px, py = player_pos
    pygame.draw.rect(screen, (0, 0, 255), [px * rect_size, py * rect_size, rect_size, rect_size])

# A* Pathfinding Algorithm
# Reference I used: https://www.geeksforgeeks.org/a-search-algorithm/#
# The heapq idea came from ChatGPT
def astar(maze, start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, end), 0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_list:
        _, current_g, current = heapq.heappop(open_list)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for direction in directions:
            nx, ny = current[0] + direction[0], current[1] + direction[1]
            if 0 <= nx < mze_width and 0 <= ny < mze_height and maze[ny][nx] == 0:
                neighbor = (nx, ny)
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_score[neighbor], tentative_g_score, neighbor))

    return []

# Player class for handling movement and current location
class Player:
    def __init__(self, start_pos, end_pos, maze, move_interval=1.0):
        self.position = start_pos
        self.end_pos = end_pos
        self.maze = maze
        self.path = astar(maze, start_pos, end_pos)
        self.current_target_index = 0
        self.last_move_time = time.time()
        self.move_interval = move_interval

    def move(self):
        if not self.path:
            return

        current_time = time.time()
        if current_time - self.last_move_time >= self.move_interval and self.current_target_index < len(self.path):
            self.position = self.path[self.current_target_index]
            self.current_target_index += 1
            self.last_move_time = current_time


maze = generate_maze(mze_width, mze_height)
player = Player(start_pos=(0, 0), end_pos=(mze_width - 2, mze_height - 2), maze=maze, move_interval=0.1)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    player.move()

    screen.fill((0, 0, 0))
    draw_maze(maze, player.position)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
