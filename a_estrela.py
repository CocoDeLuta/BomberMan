import heapq

class AEstrela:

    def __init__(self):
        pass
    
    def a_star_search_avoid_4(self, matrix, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def is_near_4(position):
            x, y = position
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]):
                    if matrix[nx][ny] == 4:
                        return True
            return False

        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                path = [goal]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()

                print("Caminho completo:", path)
                if len(path) > 1:
                    return path[1]
                else:
                    return None

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < len(matrix) and 0 <= neighbor[1] < len(matrix[0]):
                    if matrix[neighbor[0]][neighbor[1]] in [3, 4]:
                        continue

                    tentative_g_score = g_score[current] + 1

                    # Adiciona um custo extra se o vizinho estiver próximo de um 4
                    if is_near_4(neighbor):
                        tentative_g_score += 5  # Ajuste o valor do custo extra conforme necessário

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return None
