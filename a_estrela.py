import heapq

class AEstrela:

    def __init__(self):
        pass
    
    def a_star_search_avoid_4(self, matrix, start, goal):
        # Função heurística que calcula a distância de Manhattan entre dois pontos
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        # Função que verifica se uma posição está próxima de uma célula com valor 4
        def is_near_4(position):
            x, y = position
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]):
                    if matrix[nx][ny] == 4:
                        return True
            return False

        # Lista de nós abertos (a serem avaliados)
        open_list = []
        heapq.heappush(open_list, (0, start))  # Adiciona o nó inicial com custo 0
        came_from = {}  # Dicionário para rastrear o caminho
        g_score = {start: 0}  # Custo do caminho do início até o nó atual
        f_score = {start: heuristic(start, goal)}  # Custo estimado do início até o objetivo passando pelo nó atual

        while open_list:
            _, current = heapq.heappop(open_list)  # Pega o nó com menor f_score

            if current == goal:
                # Reconstrói o caminho do objetivo até o início
                path = [goal]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()

                print("Caminho completo:", path) # Só pra debugar
                if len(path) > 1:
                    return path[1]  # Retorna o próximo passo no caminho
                else:
                    return None

            # Verifica os vizinhos do nó atual
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < len(matrix) and 0 <= neighbor[1] < len(matrix[0]):
                    if matrix[neighbor[0]][neighbor[1]] in [3, 4]:
                        continue  # Ignora paredes e bombas

                    tentative_g_score = g_score[current] + 1  # Custo do caminho até o vizinho

                    # Adiciona um custo extra se o vizinho estiver próximo de uma bomba (valor 4)
                    if is_near_4(neighbor):
                        tentative_g_score += 5  # Ajuste o valor do custo extra conforme necessário

                    # Se o vizinho não foi visitado ou encontramos um caminho melhor
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))  # Adiciona o vizinho à lista aberta

        return None  # Retorna None se não houver caminho possível
